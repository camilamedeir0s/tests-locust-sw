import os
from datetime import datetime

user_count = 500
user_spawn = 50
host = "123456.us-east-2.elb.amazonaws.com"
run_time = "70s"
results_dir = "results"
#config = "distributed-distributed-2vm"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Cria o diretório para os resultados se não existir
os.makedirs(results_dir, exist_ok=True)

# Função para rodar os testes de carga com Locust
def run_locust_tests():
    #os.system(f"locust --host=http://{host} --headless --run-time={run_time} -u {user_count} -r {user_spawn} 2>&1 --csv={results_dir}/{config}/{user_count}/results_{timestamp}")
    os.system(f"locust --host=http://{host} --headless --run-time={run_time} -u {user_count} -r {user_spawn} 2>&1 --csv={results_dir}/{user_count}/results_{timestamp}")

# Execute os testes de carga
run_locust_tests()

print("Testes finalizados! :)")
