"""
Push Notification Service for APNs (Apple Push Notification service)
"""

import os
from typing import Dict, Optional
from loguru import logger
import asyncio

# APNs client (aioapns)
from aioapns import APNs, NotificationRequest, PushType

# Database
from app.database import AsyncSessionLocal
from app.models import User, DeviceToken
from sqlalchemy import select


class NotificationService:
    """Handles push notifications to iOS devices"""
    
    def __init__(self):
        self.apns_client = None
        self._initialize_apns()
    
    def _initialize_apns(self):
        """Initialize APNs client with credentials"""
        try:
            key_id = os.getenv("APNS_KEY_ID")
            team_id = os.getenv("APNS_TEAM_ID")
            bundle_id = os.getenv("APNS_BUNDLE_ID")
            key_file = os.getenv("APNS_KEY_FILE")
            use_sandbox = os.getenv("APNS_USE_SANDBOX", "true").lower() == "true"
            
            if not all([key_id, team_id, bundle_id, key_file]):
                logger.warning("APNs credentials not configured - push notifications disabled")
                return
            
            # Read the private key
            with open(key_file, 'r') as f:
                key_content = f.read()
            
            self.apns_client = APNs(
                key=key_content,
                key_id=key_id,
                team_id=team_id,
                topic=bundle_id,
                use_sandbox=use_sandbox
            )
            
            logger.info(f"APNs client initialized (sandbox: {use_sandbox})")
        
        except Exception as e:
            logger.error(f"Failed to initialize APNs: {e}")
            self.apns_client = None
    
    async def send_notification(
        self,
        device_token: str,
        title: str,
        body: str,
        data: Optional[Dict] = None,
        badge: int = 1,
        sound: str = "default"
    ) -> bool:
        """
        Send push notification to a device
        
        Args:
            device_token: APNs device token
            title: Notification title
            body: Notification body
            data: Additional custom data
            badge: Badge count
            sound: Sound file name
        
        Returns:
            True if successful, False otherwise
        """
        if not self.apns_client:
            logger.warning("APNs client not initialized - skipping notification")
            return False
        
        try:
            # Build notification payload
            notification = NotificationRequest(
                device_token=device_token,
                message={
                    "aps": {
                        "alert": {
                            "title": title,
                            "body": body
                        },
                        "badge": badge,
                        "sound": sound,
                        "content-available": 1
                    }
                },
                push_type=PushType.ALERT
            )
            
            # Add custom data if provided
            if data:
                notification.message.update(data)
            
            # Send notification
            response = await self.apns_client.send_notification(notification)
            
            if response.is_successful:
                logger.info(f"Notification sent successfully to {device_token[:10]}...")
                return True
            else:
                logger.error(f"Failed to send notification: {response.description}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return False
    
    async def send_to_user(
        self,
        user_id: str,
        title: str,
        body: str,
        data: Optional[Dict] = None
    ) -> int:
        """
        Send notification to all devices registered for a user
        
        Returns:
            Number of successful sends
        """
        async with AsyncSessionLocal() as session:
            try:
                # Get all active device tokens for user
                stmt = select(DeviceToken).where(
                    DeviceToken.user_id == user_id,
                    DeviceToken.active == True,
                    DeviceToken.platform == "ios"
                )
                
                result = await session.execute(stmt)
                tokens = result.scalars().all()
                
                if not tokens:
                    logger.info(f"No device tokens found for user {user_id}")
                    return 0
                
                # Send to all devices
                success_count = 0
                for token in tokens:
                    success = await self.send_notification(
                        device_token=token.device_token,
                        title=title,
                        body=body,
                        data=data
                    )
                    if success:
                        success_count += 1
                
                logger.info(f"Sent notifications to {success_count}/{len(tokens)} devices for user {user_id}")
                return success_count
            
            except Exception as e:
                logger.error(f"Error sending notifications to user {user_id}: {e}")
                return 0


# Singleton instance
notification_service = NotificationService()


# Convenience function
async def send_push_notification(
    user_id: str,
    title: str,
    body: str,
    data: Optional[Dict] = None
) -> bool:
    """Send push notification to user"""
    count = await notification_service.send_to_user(user_id, title, body, data)
    return count > 0


# Example usage
if __name__ == "__main__":
    async def test_notification():
        # Test notification
        result = await send_push_notification(
            user_id="test-user-id",
            title="✨ Test Notification",
            body="This is a test from Attireum",
            data={"type": "test"}
        )
        print(f"Notification sent: {result}")
    
    asyncio.run(test_notification())

