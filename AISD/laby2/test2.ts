// you can write to stdout for debugging purposes, e.g.
// console.log('this is a debug message');

let lowestCurrentScore = Infinity;

const cache = new Set<string>();

let lettersMap: Map<string, number> = new Map();
let timeCalled = 0;

const approximateScore = (P: string, Q: string): number => {
  const N = P.length;
  const pMap = new Map<string, number>();
  const qMap = new Map<string, number>();

  for (let i = 0; i < N; i++) {
    const qLetter = Q[i];
    const pLetter = P[i];
    pMap.set(pLetter, (pMap.get(pLetter) ?? 0) + 1);
    qMap.set(qLetter, (qMap.get(qLetter) ?? 0) + 1);
  }

  const lettersSet = new Set();

  for (let i = 0; i < N; i++) {
    const qLetter = Q[i];
    const pLetter = P[i];

    if (lettersSet.has(pLetter) || lettersSet.has(qLetter)) {
      continue;
    }

    const qValue = qMap.get(qLetter) ?? 0;
    const pValue = pMap.get(pLetter) ?? 0;

    if (qValue > pValue) {
      lettersSet.add(qLetter);
    } else if (pValue > qValue) {
      lettersSet.add(pLetter);
    } else {
      const combinedValueQLetter = qValue + (pMap.get(qLetter) ?? 0);
      const combinedValuePLetter = pValue + (qMap.get(pLetter) ?? 0);

      if (combinedValuePLetter > combinedValueQLetter) {
        lettersSet.add(pLetter);
      } else if (combinedValueQLetter > combinedValuePLetter) {
        lettersSet.add(qLetter);
      } else {
        lettersSet.add(qLetter);
      }
    }
  }

  return lettersSet.size;
};

const generateLetterMap = (P: string, Q: string): Map<string, number> => {
  const N = P.length;
  const map = new Map<string, number>();

  for (let i = 0; i < N; i++) {
    const qLetter = Q[i];
    const pLetter = P[i];

    if (map.has(qLetter)) {
      map.set(qLetter, map.get(qLetter)! + 1);
    } else {
      map.set(qLetter, 1);
    }

    if (map.has(pLetter)) {
      map.set(pLetter, map.get(pLetter)! + 1);
    } else {
      map.set(pLetter, 1);
    }
  }

  return map;
};

const getMinimalPossibleScore = ({
  availableLetters,
  freeSpace,
}: {
  availableLetters: Map<string, number>;
  freeSpace: number;
}) => {
  let score = 0;
  const entries = Array.from(availableLetters.entries()).sort(
    (a, b) => b[1] - a[1]
  );

  if (timeCalled % 1000 === 0) {
    console.log("timeCalled", timeCalled);
    console.log(entries);
  }

  while (freeSpace > 0) {
    const [letter, count] = entries[score];
    if (count > freeSpace) {
      return 1;
    }

    freeSpace -= count;
    score++;
  }

  return score;
};

const getScore = ({
  P,
  Q,
  currentString,
  availableLetters,
  freeSpace = P.length,
}: {
  P: string;
  Q: string;
  currentString: (string | undefined)[];
  availableLetters: Map<string, number>;
  freeSpace?: number;
}): number => {
  const cacheKey = currentString.map((letter) => letter || "_").join("");

  if (cache.has(cacheKey)) {
    return Infinity;
  }

  timeCalled++;

  cache.add(cacheKey);

  const uniqueLetters = new Set(currentString);
  uniqueLetters.delete(undefined);

  const minimalAdditionalScore = getMinimalPossibleScore({
    availableLetters,
    freeSpace,
  });

  const currentScore = uniqueLetters.size + minimalAdditionalScore;

  if (timeCalled % 1000 === 0) {
    console.log(
      "string",
      currentString.map((letter) => letter || "_").join("")
    );
    console.log("currentScore", currentScore);
    console.log("lowestScore", lowestCurrentScore);
  }

  if (currentScore >= lowestCurrentScore) {
    return lowestCurrentScore;
  }

  if (currentString.every((letter) => letter !== undefined)) {
    if (currentScore < lowestCurrentScore) {
      lowestCurrentScore = currentScore;
    }

    return lowestCurrentScore;
  }

  if (availableLetters.size === 0) {
    return Infinity;
  }

  const sortedKeys = Array.from(availableLetters.keys()).sort((a, b) => {
    const aLetterCount = availableLetters.get(a) ?? 0;
    const bLetterCount = availableLetters.get(b) ?? 0;

    return bLetterCount - aLetterCount;
  });

  for (let letter of sortedKeys) {
    let freeSpace = 0;
    const stringCopy = [...currentString];
    const lettersMap2 = new Map<string, number>();

    for (let i = 0; i < stringCopy.length; i++) {
      if (stringCopy[i] === undefined) {
        if (P[i] === letter) {
          stringCopy[i] = letter;
        } else if (Q[i] === letter) {
          stringCopy[i] = letter;
        } else {
          freeSpace++;
        }

        for (let letterNew of sortedKeys) {
          const pLetter = P[i];
          const qLetter = Q[i];
          if (P[i] === letterNew) {
            if (lettersMap2.has(pLetter)) {
              lettersMap2.set(pLetter, lettersMap2.get(pLetter)! + 1);
            } else {
              lettersMap2.set(pLetter, 1);
            }
          } else if (Q[i] === letterNew) {
            if (lettersMap2.has(qLetter)) {
              lettersMap2.set(qLetter, lettersMap2.get(qLetter)! + 1);
            } else {
              lettersMap2.set(qLetter, 1);
            }
          }
        }
      }
    }

    lettersMap2.delete(letter);

    if (lettersMap2.size === 0) {
      continue;
    }

    const score = getScore({
      P,
      Q,
      freeSpace,
      currentString: stringCopy,
      availableLetters: lettersMap,
    });

    if (score < lowestCurrentScore) {
      lowestCurrentScore = score;
    }
  }

  return lowestCurrentScore;
};

function solution(P: string, Q: string): number {
  console.time("solution");

  lowestCurrentScore = approximateScore(P, Q);

  const stringTemplate = new Array<string | undefined>(P.length).fill(
    undefined
  );

  lettersMap = generateLetterMap(P, Q);

  const score = getScore({
    P,
    Q,
    availableLetters: lettersMap,
    currentString: stringTemplate,
  });

  console.timeEnd("solution");

  console.log("timeCalled", timeCalled);

  return score;
}
