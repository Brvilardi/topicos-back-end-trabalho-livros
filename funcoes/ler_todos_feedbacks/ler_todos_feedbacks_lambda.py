from shared.repositorios.feedback_dynamo_repository import FeedbacksRepositoryDynamo
from shared.entidades import Feedback
from shared.http.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from uuid import uuid4

feedback_repository = FeedbacksRepositoryDynamo()


def lambda_handler(event, context):


    feedbacks = feedback_repository.get_todos_feedback()

    if len(feedbacks) == 0:
        raise Exception("Nenhum feedback encontrado")

    
    httpResponse = LambdaHttpResponse(
        status_code=200,
        body={
            "message": "Feedbacks lidos com sucesso!",
            "feedbacks": [feedback.to_dict() for feedback in feedbacks]
        }
    )


    return httpResponse.toDict()