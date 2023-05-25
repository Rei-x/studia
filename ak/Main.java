public class Main {
  public static void main(String[] args) {
    int N = 50;
    int[] numall = new int[N];
    int[] primes = new int[N];
    int nprimes = 0;

    for (int i = 0; i < N; i++) {
      numall[i] = i;
    }

    int n = 2;
    int limit = N / 2;

    while (n < limit) {
      int j = n * 2;
      while (j < N) {
        numall[j] = 0;
        j += n;
      }
      n++;
    }

    int i = 1;
    int count = 0;

    while (i < N) {
      if (numall[i] != 0) {
        primes[count] = numall[i];
        count++;
      }
      i++;
    }

    nprimes = count;

    for (i = 0; i < count; i++) {
      System.out.print(" ");
      System.out.print(primes[i]);
    }

    System.out.println();
  }
}
