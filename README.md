## Multicloud Automation with python

This is the repository for the code to this Blog post.


### Installation 

- Fill out the configuration files: 

#### AWS

```
cloud: aws
access_key: 1234
secret_key: 1234
worker_size: t2.micro
region: eu-central-1
image_id: ami-01a724a06f336afd8
security_group: sg-0611318194634a93d
subnet_id: subnet-05390973cac1638bd
```

#### Digitalocean

```
cloud: do
do_key: 1234
worker_size: s-1vcpu-1gb
region: fra1
image_id: '13371338'
```

```
docker build . -t automation 

docker run -it --rm -v "$(pwd):/code" automation bash
```