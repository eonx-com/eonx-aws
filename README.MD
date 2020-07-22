# EonX Python AWS Library

This repository contains a library of reusable AWS classes designed to take some of the annoyance out of using the Boto3 library. It is by no means complete
as modules have only been added as required by projects.

* CloudWatch
    * put_metric
    * increment_count    
* EC2
    * describe_regions
* ECS
    * list_clusters
    * describe_cluster
    * list_services
    * describe_service
    * list_tasks
    * describe_task
    * list_task_definitions
    * describe_task_definition
    * run_task
* Lambda
    * invoke
* Quantum Ledger Database
    * create_ledger
    * delete_ledger
    * describe_ledger
    * list_ledgers    
* Route53
    * list_hosted_zones_by_id
    * list_hosted_zones_by_name
    * create_name_server_record
