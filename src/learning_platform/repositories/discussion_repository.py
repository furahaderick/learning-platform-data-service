from datetime import datetime, timezone
from bson.objectid import ObjectId


class DiscussionRepository:
    def __init__(self, mongo_database):
        self.collection = mongo_database["discussions"]

    def create_thread(self, course_id, student_id, message):
        document = {
            "course_id": course_id,
            "student_id": student_id,
            "message": message,
            "created_at": datetime.now(timezone.utc),
            "replies": [],
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def add_reply(self, thread_id, student_id, message):
        result = self.collection.update_one(
            {"_id": ObjectId(thread_id)},
            {
                "$push": {
                    "replies": {
                        "student_id": student_id,
                        "message": message,
                        "created_at": datetime.now(timezone.utc),
                    }
                }
            },
        )
        return result.modified_count > 0

    def get_course_threads(self, course_id):
        return list(
            self.collection.find({"course_id": course_id}).sort("created_at", -1)
        )
