import pytest
from app.database.models.user import User
from app.database.models.memory import Memory
from app.database.models.conversation import Conversation
from app.database.models.enrollment import Enrollment
from app.database.models.embedding import Embedding
from app.database.models.summary import Summary
from app.database.models.follow_up import FollowUp
from app.database.models.admin_log import AdminLog
from app.database.models.message import Message
from app.database.models.lead_status import LeadStatusHistory

class TestModels:
    def test_user_model(self):
        assert User.__tablename__ == "users"
        assert hasattr(User, 'telegram_id')
        assert hasattr(User, 'lead_status')
        assert hasattr(User, 'is_enrolled')

    def test_memory_model(self):
        assert Memory.__tablename__ == "memories"
        assert hasattr(Memory, 'key')
        assert hasattr(Memory, 'value')
        assert hasattr(Memory, 'category')

    def test_conversation_model(self):
        assert Conversation.__tablename__ == "conversations"
        assert hasattr(Conversation, 'role')
        assert hasattr(Conversation, 'content')

    def test_enrollment_model(self):
        assert Enrollment.__tablename__ == "enrollments"
        assert hasattr(Enrollment, 'full_name')
        assert hasattr(Enrollment, 'status')

    def test_embedding_model(self):
        assert Embedding.__tablename__ == "embeddings"
        assert hasattr(Embedding, 'content')
        assert hasattr(Embedding, 'embedding')

    def test_summary_model(self):
        assert Summary.__tablename__ == "summaries"
        assert hasattr(Summary, 'summary')
        assert hasattr(Summary, 'key_points')

    def test_follow_up_model(self):
        assert FollowUp.__tablename__ == "follow_ups"
        assert hasattr(FollowUp, 'status')
        assert hasattr(FollowUp, 'scheduled_at')

    def test_admin_log_model(self):
        assert AdminLog.__tablename__ == "admin_logs"
        assert hasattr(AdminLog, 'admin_id')
        assert hasattr(AdminLog, 'action')

    def test_lead_status_model(self):
        assert LeadStatusHistory.__tablename__ == "lead_status_history"
        assert hasattr(LeadStatusHistory, 'old_status')
        assert hasattr(LeadStatusHistory, 'new_status')
