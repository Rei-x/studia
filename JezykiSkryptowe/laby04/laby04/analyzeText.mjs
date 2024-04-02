// @ts-check
import { promises as fs } from "node:fs";
import { createInterface } from "node:readline";
import * as path from "node:path";
/**
 * Represents the result of text analysis.
 * @typedef {Object} AnalysisResult
 * @property {string} path - The absolute path of the analyzed text file.
 * @property {number} totalCharacters - The total number of characters in the text.
 * @property {number} totalWords - The total number of words in the text.
 * @property {number} totalLines - The total number of lines in the text.
 * @property {Object} mostFrequentCharacter - The most frequent character in the text.
 * @property {string} mostFrequentCharacter.character - The most frequent character.
 * @property {number} mostFrequentCharacter.frequency - The frequency of the most frequent character.
 * @property {Object} mostFrequentWord - The most frequent word in the text.
 * @property {string} mostFrequentWord.word - The most frequent word.
 * @property {number} mostFrequentWord.frequency - The frequency of the most frequent word.
 */

/**
 * Analyzes a text file and calculates various statistics such as total characters, total words,
 * total lines, character frequency, word frequency, most frequent character, and most frequent word.
 * @param {string} filePath - The path to the text file.
 * @returns {Promise<AnalysisResult>} - A promise that resolves once the analysis is complete.
 */
const analyzeFile = async (filePath) => {
  const absolutePath = path.resolve(filePath);

  const data = await fs.readFile(filePath, "utf8");

  const totalCharacters = data.length;
  const words = data.split(/\s+/).filter(Boolean);
  const totalWords = words.length;
  const totalLines = data.split("\n").length;

  /**
   * @type {Map<string, number>} - A map that stores the frequency of each character in the text.
   */
  const characterFrequency = new Map();
  for (const char of data) {
    if (!/\s/.test(char)) {
      // Ignoring whitespace for character frequency
      characterFrequency.set(char, (characterFrequency.get(char) ?? 0) + 1);
    }
  }

  /**
   * @type {Map<string, number>} - A map that stores the frequency of each character in the text.
   */
  const wordFrequency = new Map();
  for (const word of words.map((word) => word.toLowerCase())) {
    wordFrequency.set(word, (wordFrequency.get(word) ?? 0) + 1);
  }

  const mostFrequentCharacter =
    characterFrequency.size > 0
      ? [...characterFrequency.entries()].reduce((a, b) =>
          a[1] > b[1] ? a : b
        )
      : undefined;

  const mostFrequentWord =
    wordFrequency.size > 0
      ? [...wordFrequency.entries()].reduce((a, b) => (a[1] > b[1] ? a : b))
      : undefined;

  /** @type {AnalysisResult} */
  const result = {
    path: absolutePath,
    totalCharacters,
    totalWords,
    totalLines,
    mostFrequentCharacter: mostFrequentCharacter?.at(0),
    characterFrequency: mostFrequentCharacter?.at(1),
    mostFrequentWord: mostFrequentWord?.at(0),
    wordFrequency: mostFrequentWord?.at(1),
  };

  return result;
};

for await (const line of createInterface({ input: process.stdin })) {
  console.log(JSON.stringify(await analyzeFile(line)));
}
