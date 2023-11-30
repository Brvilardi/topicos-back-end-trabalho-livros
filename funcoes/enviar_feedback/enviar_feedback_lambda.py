from shared.repositorios.feedback_dynamo_repository import FeedbacksRepositoryDynamo
from shared.entidades import Feedback
from shared.http.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from uuid import uuid4




def lambda_handler(event, context):

    httpRequest = LambdaHttpRequest(data=event)

    httpRequest.body["id"] = str(uuid4())
    
    feedback = Feedback.from_dict(httpRequest.body)

    feedback_repository = FeedbacksRepositoryDynamo()

    feedback_repository.create_feedback(feedback)

    
    httpResponse = LambdaHttpResponse(
        status_code=200,
        body={
            "message": "Feedback enviado com sucesso!",
            "feedback": feedback.to_dict()
        }
    )


    return httpResponse.toDict()