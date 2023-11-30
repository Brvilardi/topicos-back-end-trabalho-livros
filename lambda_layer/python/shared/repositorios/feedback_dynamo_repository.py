from decimal import Decimal
from typing import List
from shared.entidades import Feedback

from shared.repositorios.dynamo_datasource import DynamoDatasource

import os

DYNAMO_TABLE = os.environ.get('DYNAMO_TABLE')
AWS_REGION = os.environ.get('AWS_REGION')



class FeedbacksRepositoryDynamo:

    @staticmethod
    def partition_key_format(id) -> str:
        return f"feedback#{id}"

    def __init__(self):
        self.dynamo = DynamoDatasource(dynamo_table_name=DYNAMO_TABLE,
                                       region=AWS_REGION,
                                       partition_key="PK")
        
    def create_feedback(self, new_feedback: Feedback) -> Feedback:

        resp = self.dynamo.put_item(partition_key=self.partition_key_format(new_feedback.id),
            item=new_feedback.to_dict()
                                    )
        return new_feedback
    
    def get_feedback_by_id(self, feedback_id: str) -> Feedback:
        resp = self.dynamo.get_item(partition_key=self.partition_key_format(feedback_id))

        if resp.get('Item') is None:
            raise Exception("feedback_id does not exist")
        
        item = resp["Item"]
        item["classificacao"] = float(item["classificacao"])
        
        feedback = Feedback.from_dict(item)
        return feedback
    
    def get_todos_feedback(self) -> List[Feedback]:
        resp = self.dynamo.get_all_items()
        print("Dynamo response:")
        print(resp)

        feedbacks = []
        for item in resp['Items']:
            item["classificacao"] = float(item["classificacao"])
            feedbacks.append(Feedback.from_dict(item))

        return feedbacks
        


    # def get_all_user(self) -> List[User]:
    #     resp = self.dynamo.get_all_items()
    #     users = []
    #     for item in resp['Items']:
    #         if item.get("entity") == 'user':
    #             users.append(UserDynamoDTO.from_dynamo(item).to_entity())

    #     return users


    # def create_user(self, new_user: User) -> User:
    #     print(f"repo entered.\n Repo:{self}")
    #     print(self.dynamo.dynamo_table.__dict__)
    #     new_user.user_id = self.get_user_counter()
    #     print(f"nre user id: {new_user.user_id}")
    #     user_dto = UserDynamoDTO.from_entity(user=new_user)
    #     resp = self.dynamo.put_item(partition_key=self.partition_key_format(new_user.user_id),
    #                                 sort_key=self.sort_key_format(user_id=new_user.user_id), item=user_dto.to_dynamo(),
    #                                 is_decimal=True)
    #     return new_user

    # def delete_user(self, user_id: int) -> User:
    #     resp = self.dynamo.delete_item(partition_key=self.partition_key_format(user_id), sort_key=self.sort_key_format(user_id))

    #     if "Attributes" not in resp:
    #         raise NoItemsFound("user_id")

    #     return UserDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    # def update_user(self, user_id: int, new_name: str) -> User:

    #     user = self.get_user(user_id=user_id)

    #     item_to_update = {}

    #     if new_name:
    #         item_to_update['name'] = new_name
    #     else:
    #         raise NoItemsFound("Nothing to update")

    #     resp = self.dynamo.update_item(partition_key=self.partition_key_format(user_id), sort_key=self.sort_key_format(user_id), update_dict=item_to_update)

    #     return UserDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    # def get_user_counter(self) -> int:

    #     return self.update_counter()

    # def update_counter(self) -> int: #TODO fix this
    #     print("updating counter")
    #     counter = int(self.dynamo.get_item(partition_key='COUNTER', sort_key='COUNTER')['Item']['COUNTER'])
    #     print(f"counter: {counter}")
    #     resp = self.dynamo.update_item(partition_key='COUNTER', sort_key='COUNTER', update_dict={'COUNTER': Decimal(counter+1)})
    #     print(f"resp: {resp}")

    #     return int(resp['Attributes']['COUNTER'])