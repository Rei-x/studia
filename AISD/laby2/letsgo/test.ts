let lowestCurrentScore = Infinity;

let timesCalled = 0;

const getScore = ({
  P,
  Q,
  currentString = "",
  currentIndex = 0,
}: {
  P: string;
  Q: string;
  currentString?: string;
  currentIndex?: number;
}): number => {
  const currentScore = new Set(currentString).size;

  if (currentScore >= lowestCurrentScore) {
    return lowestCurrentScore;
  }

  timesCalled++;

  if (currentString.length === P.length) {
    if (new Set(currentString).size < lowestCurrentScore) {
      lowestCurrentScore = new Set(currentString).size;
    }

    return new Set(currentString).size;
  } else {
    const pValue = getScore({
      P,
      Q,
      currentString: currentString + P[currentIndex],
      currentIndex: currentIndex + 1,
    });
    const qValue = getScore({
      P,
      Q,
      currentString: currentString + Q[currentIndex],
      currentIndex: currentIndex + 1,
    });

    return Math.min(pValue, qValue);
  }
};

function solution(P: string, Q: string): number {
  console.time("solution");
  const pScore = new Set(P).size;
  const qScore = new Set(Q).size;

  lowestCurrentScore = Math.min(pScore, qScore);

  const score = getScore({ P, Q });
  console.timeEnd("solution");
  console.log("timesCalled", timesCalled);
  return score;
}
