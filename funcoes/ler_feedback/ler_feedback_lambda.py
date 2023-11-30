from shared.repositorios.feedback_dynamo_repository import FeedbacksRepositoryDynamo
from shared.entidades import Feedback
from shared.http.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from uuid import uuid4
from pprint import pprint

feedback_repository = FeedbacksRepositoryDynamo()


def lambda_handler(event, context):

    httpRequest = LambdaHttpRequest(data=event)
    
    feedback_id = httpRequest.query_params.get("feedback_id")

    feedback = feedback_repository.get_feedback_by_id(feedback_id)

    pprint(feedback.to_dict())


    
    httpResponse = LambdaHttpResponse(
        status_code=200,
        body={
            "message": "Feedback lido com sucesso!",
            "feedback": feedback.to_dict()
        }
    )


    return httpResponse.toDict()