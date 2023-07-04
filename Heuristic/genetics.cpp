#include <bits/stdc++.h>
#define MAX 1000
#define MIN_RUNNING_TIME 10 // Run at least 10 seconds, if not found feasible(chap nhan dc) solution then continue to run
#define POPULATION_SIZE 100  // Sl quan the
#define MUTATION_RATE 0.05 // Dot bien
using namespace std;
void input();
int *gen_chromosome();
int N, M, K;
int a, b, c, d, e, f;
int **thesis_similarity;
int **teacher_thesis_similarity;
int *advisors;
int cnt = 0;
class Assignment {
public:
  int thesis[MAX];
  int teacher[MAX];
  int fitness;
  Assignment(int chromosome[]);
  int cal_fitness();
  int check_valid();
  Assignment mate(Assignment parent2);
};
Assignment::Assignment(int chromosome[]) {
  for (int i = 0; i < N; i++) {
    this->thesis[i] = chromosome[i];
  }
  for (int i = 0; i < M; i++) {
    this->teacher[i] = chromosome[N + i];
  }
  this->fitness = cal_fitness();
}
int Assignment::cal_fitness() {
  if (check_valid() < 0) {
    return check_valid();
  }
  int score = 0;
  for (int i = 0; i < N; i++) {
    for (int j = i + 1; j < N; j++) {
      score += thesis_similarity[i][j] * (thesis[i] == thesis[j]);
    }
  }
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      score += teacher_thesis_similarity[i][j] * (thesis[i] == teacher[j]);
    }
  }

  return score;
}
int Assignment::check_valid() {
  int thesis_count[MAX] = {0};
  int teacher_count[MAX] = {0};
  int temp = 0;
  // Teacher should not in the same council with the thesis he/she is assigned
  for (int i = 0; i < N; i++) {
    if (thesis[i] == teacher[advisors[i] - 1]) {
      temp -= 1;
    }
  }
  for (int i = 0; i < N; i++) {
    thesis_count[thesis[i] - 1]++;
  }
  for (int i = 0; i < M; i++) {
    teacher_count[teacher[i] - 1]++;
  }
  for (int i = 0; i < K; i++) {
    // Thesis count in each group must be in range [a, b]

    if (thesis_count[i] < a || thesis_count[i] > b) {
      temp -= max(thesis_count[i] - b, 1);
    }
    // Teacher count in each group must be in range [c, d]
    if (teacher_count[i] < c || teacher_count[i] > d) {
      temp -= max(teacher_count[i] - d, 1);
    }
  }

  // Similarity between thesis in the same council must be at least e
  for (int i = 0; i < N; i++) {
    for (int j = i + 1; j < N; j++) {
      if ((thesis[i] == thesis[j]) && (thesis_similarity[i][j] < e)) {
        temp -= 1;
        break;
      }
    }
  }
  // Similarity between thesis and teacher must be at least f, if same council
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      if ((thesis[i] == teacher[j]) && (teacher_thesis_similarity[i][j] < f)) {
        temp -= 1;
        break;
      }
    }
  }

  return temp;
}
// sort by fitness
bool operator<(const Assignment &a, const Assignment &b) {
  return a.fitness > b.fitness;
}
Assignment Assignment::mate(Assignment parent2) {
  int *child_chromosome = new int[N + M];
  static std::random_device rd;
  static std::mt19937 gen(rd());
  std::uniform_int_distribution<int> distribution(0, 1);
  for (int i = 0; i < N; i++) {
    if (distribution(gen)) {
      child_chromosome[i] = this->thesis[i];
    } else {
      child_chromosome[i] = parent2.thesis[i];
    }
  }
  for (int i = 0; i < M; i++) {
    if (distribution(gen)) {
      child_chromosome[N + i] = this->teacher[i];
    } else {
      child_chromosome[N + i] = parent2.teacher[i];
    }
  }
  // Randomly mutate some genes
  for (int i = 0; i < N + M; i++) {
    if (rand() % 100 < MUTATION_RATE) {
      child_chromosome[i] = rand() % K + 1;
    }
  }
  return Assignment(child_chromosome);
}
void allocate() {
  thesis_similarity = new int *[N];
  for (int i = 0; i < N; i++) {
    thesis_similarity[i] = new int[N];
  }
  teacher_thesis_similarity = new int *[N];
  for (int i = 0; i < N; i++) {
    teacher_thesis_similarity[i] = new int[M];
  }
  advisors = new int[N];
}
void input() {
  freopen("input.txt", "r", stdin);
  cin >> N >> M >> K;
  cin >> a >> b >> c >> d >> e >> f;
  allocate();

  for (int i = 0; i < N; i++) {
    for (int j = 0; j < N; j++) {
      cin >> thesis_similarity[i][j];
    }
  }
  for (int i = 0; i < N; i++) {
    for (int j = 0; j < M; j++) {
      cin >> teacher_thesis_similarity[i][j];
    }
  }
  for (int i = 0; i < N; i++) {
    cin >> advisors[i];
  }
}
// gen chromosome
int *gen_chromosome() {
  static std::random_device rd;
  static std::mt19937 gen(rd());
  std::uniform_int_distribution<int> distribution(1, K);
  int *chromosome = new int[N + M];
  for (int i = 0; i < N; i++) {
    chromosome[i] = distribution(gen);
  }
  for (int i = 0; i < M; i++) {
    chromosome[N + i] = distribution(gen);
  }
  return chromosome;
}
int main() {
  input();

  int generation = 0;
  vector<Assignment> population;

  for (int i = 0; i < POPULATION_SIZE; i++) {
    population.push_back(Assignment(gen_chromosome()));
  }
  sort(population.begin(), population.end());
  int max_fitness = 0;
  // stop the loop when time is more than 25s
  // calculate time
  time_t start = time(0);
  double duration = MIN_RUNNING_TIME;
  while (max_fitness == 0 || duration > 0) {
    time_t end = time(0);
    time_t time_taken = end - start;
    duration = MIN_RUNNING_TIME - time_taken;
    sort(population.begin(), population.end());
    vector<Assignment> new_population;
    for (int i = 0; i < POPULATION_SIZE / 2; i++) {
      new_population.push_back(population[i]);
    }
    for (int i = 0; i < POPULATION_SIZE / 2; i++) {
      int parent1 = rand() % POPULATION_SIZE / 2;
      int parent2 = rand() % POPULATION_SIZE / 2;
      // check if children is different from parents
      while (parent1 == parent2) {
        parent2 = rand() % POPULATION_SIZE / 2;
      }
      new_population.push_back(population[parent1].mate(population[parent2]));
    }
    population = new_population;
    generation++;
    // Update max fitness
    if (population[0].fitness > max_fitness) {
      max_fitness = population[0].fitness;
    }
    // Print the debug info
    cout << "Generation: " << generation << endl;
    cout << "Fitness: " << population[0].fitness << endl;
    cout << "Time: " << duration << endl;
    for (int i = 0; i < N; i++) {
      cout << population[0].thesis[i] << " ";
    }
    cout << endl;
    for (int i = 0; i < M; i++) {
      cout << population[0].teacher[i] << " ";
    }
  }
  // print the best assignment
  cout << N << endl;
  for (int i = 0; i < N; i++) {
    cout << population[0].thesis[i] << " ";
  }
  cout << endl;
  cout << M << endl;
  for (int i = 0; i < M; i++) {
    cout << population[0].teacher[i] << " ";
  }
  cout << endl;
  return 0;
}