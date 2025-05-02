#!/usr/bin/env nextflow

nextflow.enable.dsl=2

params.dsn_file = 'data/dsn.txt'
params.out_dir = 'results'

process runPythonExample {
    publishDir '.', mode: 'copy'
    tag 'Run python-example container'

    container 'entsupml/python-example:4'

    input:
    path dsn_file

    output:
    path 'result.txt', emit: result

    script:
    """
    mkdir -p /data
    cp ${dsn_file} /data/dsn.txt
    python3 /app/query.py
    cp /data/result.txt result.txt
    """
}

workflow {
    runPythonExample(file(params.dsn_file))
}
