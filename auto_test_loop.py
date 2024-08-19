import os, time
from datetime import datetime

initial_user_count = 1000
final_user_count = 5000
increment = 1000
user_spawn = 40

host = "123456.us-east-2.elb.amazonaws.com"
run_time = "70s"
results_dir = "results"
config = "distributed-1vm"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Cria o diretório para os resultados se não existir
os.makedirs(results_dir, exist_ok=True)

# Função para rodar os testes de carga com Locust
def run_locust_tests(user_count):
    os.system(f"locust --host=http://{host} --headless --run-time={run_time} -u {user_count} -r {user_spawn} 2>&1 --csv={results_dir}/{config}/{user_count}/results_{timestamp}")

# Loop para executar os testes de carga com diferentes valores de user_count
for user_count in range(initial_user_count, final_user_count + increment, increment):
    print(f"Iniciando teste com {user_count} usuários e {run_time} segundos...")
    run_locust_tests(user_count)
    user_spawn += 10
    if(user_count == 4000):
        time.sleep(30)
    time.sleep(90)

print("Testes finalizados! :)")
