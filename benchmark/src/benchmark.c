/**
 * file: benchmark.c
 * author: Icko Iben
 * project: SeaQuail
 *
 * date modified:      11/27/2024
 *   - Initial completion of benchmark script
 *
 * This program runs benchmark tests with different amounts of chunk sizes
 * and processes numbers when processing large files.
 *
 * We take the configuration that has the least time and save that chunk
 * size and number of processes in dbSetup/services/processconfig.py.
 * */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <float.h>

typedef struct Bench {
  int chunkSize;
  int scalar;
  double timeElapsed;
} benchmark_t;

 /**
  * update_processconfig
  *
  * Updates our processconfig file with the number of chunks and
  * number of process our services will use when reading large
  * files.
  *
  * Parameters:
  *   - chunkSize: size of each chunk
  *   - numProcesses: number of processes to use
  *
  * Output:
  *   - none
  * */
void update_processconfig(int chunkSize, const char numProcesses[])
{
  FILE *file;

  if(NULL == (file = fopen("dbSetup/services/processconfig.py", "w"))) {
    perror("Could not open processconfig.py");
    exit(EXIT_FAILURE);
  }

  /* Write to file */
  fprintf(file, "# Auto-generated configuration file\n");
  fprintf(file, "import os\n");
  fprintf(file, "CHUNK_SIZE = %d\n", chunkSize);
  fprintf(file, "NUM_PROCESSES = %s\n", numProcesses);

  fclose(file);

  printf("Updated processconfig.py with\n  CHUNKSIZE = %d\n  NUM_PROCESSES = %s\n",
         chunkSize, numProcesses);
}

 /**
  * run_updatedb
  *
  * Runs the update_db script. Re-seeds our database to stabalize results.
  *
  * Parameters:
  *   - none
  *
  * Output:
  *   - none
  * */
double run_updatedb(void)
{
  time_t tic, toc;
  double cpu_time_used;
  int result;

  /* Re-seed database with initial values to stabalize results */
  printf("Re-seeding database\n");
  result = system("mysql -uroot -ppassword seaquail < dbSetup/static/seaquail_dump.sql");
  if (result != 0) {
    fprintf(stderr, "Error re-seeding database. Exit code: %d\n", result);
    exit(EXIT_FAILURE);
  }

  /* Start timing */
  time(&tic);

  /* Run the Python script */
  result = system("python3 dbSetup/update_db.py appearances fielding batting");
  if (result != 0) {
    fprintf(stderr, "Error running update_db.py script. Exit code: %d\n", result);
    fprintf(stderr, "Are you running in a python virtual environment?\n");
    exit(EXIT_FAILURE);
  }

  /* End timing */
  time(&toc);
  cpu_time_used = difftime(toc, tic);

  return cpu_time_used;
}

 /**
  * main
  *
  * Runs all combinations of chunk sizes and number of processes.
  * Finds the fastest combination and saves that in processconfig.
  *
  * Parameters:
  *   - none
  *
  * Output:
  *   - none
  * */
int main(void)
{
  const int chunkSizes[] = {1000, 5000, 10000, 25000};
  const int processScalars[] = {1, 2, 4, 8};
  benchmark_t *benchmarks;
  double fastestTime = DBL_MAX;
  int fastestChunk = 0;
  char fastestProcess[80] = {0};
  int i, j;
  FILE *log_file;

  /* Open a file to log the results */
  log_file = fopen("benchmark_results.txt", "w");
  if (log_file == NULL) {
    perror("Error opening benchmark_results.txt");
    exit(EXIT_FAILURE);
  }

  benchmarks = malloc(
            sizeof(benchmark_t)
            * (sizeof(chunkSizes) / sizeof(chunkSizes[0]))
            * (sizeof(processScalars) / sizeof(processScalars[0]))
  );

  if(benchmarks == NULL) {
    perror("Failed malloc");
    exit(EXIT_FAILURE);
  }

  fprintf(log_file, "%-12s%-32s%10s\n", "NUM_CHUNKS", "NUM_PROCESSES", "TIME(s)");

  /* Iterate over all combinations of chunk sizes and number of cores */
  for (i = 0; i < (int)(sizeof(chunkSizes) / sizeof(chunkSizes[0])); i++) {
    for (j = 0; j < (int)(sizeof(processScalars) / sizeof(processScalars[0])); j++) {
      char numProcesses[80];

      benchmarks->chunkSize = chunkSizes[i];
      benchmarks->scalar = processScalars[j];

      /**
       * We dynamically calculate the number of processes using the number
       * of cores on the current machine. If the number of cores cannot
       * be determined using os.cpu_count, we use 4 as the default scalar.
       * */
      sprintf(numProcesses, "(os.cpu_count() or 4) * %d", benchmarks->scalar);

      /* Update processconfig.py */
      update_processconfig(benchmarks->chunkSize, numProcesses);

      /* Run the script and measure the time */
      benchmarks->timeElapsed = run_updatedb();

      /* Log the results */
      fprintf(log_file, "%-12d%-32s%10.2f\n", benchmarks->chunkSize, numProcesses, benchmarks->timeElapsed);
      printf("CHUNK_SIZE=%d, NUM_PROCESSES=%s, TIME=%.2f seconds\n", benchmarks->chunkSize, numProcesses, benchmarks->timeElapsed);

      /* Save fastest */
      if(benchmarks->timeElapsed < fastestTime) {
        fastestTime = benchmarks->timeElapsed;
        fastestChunk = benchmarks->chunkSize;
        strncpy(fastestProcess, numProcesses, 80);
      }
    }
  }

  fclose(log_file);
  free(benchmarks);

  /* Save fastest config to processconfig.py */
  printf("\nFastest configuration: CHUNK_SIZE=%d, NUM_PROCESSES=%s, TIME=%.2f seconds\n",
         fastestChunk, fastestProcess, fastestTime);

  update_processconfig(fastestChunk, fastestProcess);
  printf("Updated processconfig.py with the fastest configuration.\n");

  return EXIT_SUCCESS;
}
