import kfp
from kfp import dsl
from kubernetes import client as k8s_client

def synthetic_data_generation_op(input_path, output_path):
    return dsl.ContainerOp(
        name='Synthetic Data Generation',
        image='python:3.8-slim',
        command=['python', 'synthetic_data_generation.py'],
        arguments=[
            '--input_path', input_path,
            '--output_path', output_path
        ],
        file_outputs={}
    ).add_volume_mount(
        k8s_client.V1VolumeMount(
            mount_path='/root/.aws',
            name='aws-creds',
            read_only=True
        )
    ).add_volume(
        k8s_client.V1Volume(
            name='aws-creds',
            secret=k8s_client.V1SecretVolumeSource(secret_name='aws-secret')
        )
    )

@dsl.pipeline(
    name='Synthetic Data Pipeline',
    description='An example pipeline that generates synthetic data and trains a model.'
)
def synthetic_data_pipeline(input_path: str, output_path: str):
    generate_task = synthetic_data_generation_op(input_path, output_path)
  

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(synthetic_data_pipeline, 'synthetic_data_pipeline.yaml')
