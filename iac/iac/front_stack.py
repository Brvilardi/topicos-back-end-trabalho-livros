
from aws_cdk import (
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    RemovalPolicy
)
from constructs import Construct



class FrontEnd(Construct):
    s3_bucket: s3.Bucket
    cloudfront_distribution: cloudfront.Distribution

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.s3_bucket = s3.Bucket(self, "FrontEndBucket",
                                    bucket_name="feedbacks-front-t2-1234",
                                      removal_policy=RemovalPolicy.DESTROY,
                                        auto_delete_objects=True,
                                        )
        
        self.cloudfront_distribution = cloudfront.Distribution(self, "FrontEndDistribution",
                                                                default_behavior=cloudfront.BehaviorOptions(
                                                                    origin= cloudfront_origins.S3Origin(
                                                                        self.s3_bucket,
                                                                        origin_path="index.html"
                                                                    )
                                                                )
        )

        
        
        
    

