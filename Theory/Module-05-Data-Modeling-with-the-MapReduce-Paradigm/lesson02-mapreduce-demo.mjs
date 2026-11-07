// A small, single-process teaching simulation, not a distributed runtime.
// Keys are strings or arrays of strings; values are small in-memory examples.
export function groupByKey(pairs) {
    const groups = new Map();
    for (const [key, value] of pairs) {
        const encoded = JSON.stringify(key);
        if (!groups.has(encoded)) groups.set(encoded, { key, values: [] });
        groups.get(encoded).values.push(value);
    }
    return [...groups.values()];
}

export function simulate(partitions, mapper, reducer, combiner = null) {
    let mappedPairs = 0;
    const intermediate = [];
    for (const records of partitions) {
        const pairs = records.flatMap(mapper);
        mappedPairs += pairs.length;
        if (combiner) {
            intermediate.push(...groupByKey(pairs).map(
                ({ key, values }) => [key, combiner(values)]
            ));
        } else {
            intermediate.push(...pairs);
        }
    }
    const grouped = groupByKey(intermediate);
    const results = grouped.map(({ key, values }) => [key, reducer(values)]);
    return { mappedPairs, shuffledPairs: intermediate.length, grouped, results };
}

export const sum = values => values.reduce((total, value) => total + value, 0);
export const wordMap = line => line.trim()
    ? line.trim().split(/\s+/).map(word => [word, 1])
    : [];

// day is already parsed and validated using an agreed timezone.
// Duplicate event IDs must be resolved upstream under a stated policy.
export const failedLoginMap = event => event.status === 'failure'
    ? [[[event.user, event.day], 1]]
    : [];

export const mergeStats = pairs => pairs.reduce(
    ([total, count], [partialTotal, partialCount]) =>
        [total + partialTotal, count + partialCount],
    [0, 0]
);
export const meanStats = pairs => {
    const [total, count] = mergeStats(pairs);
    return count ? total / count : null;
};

const words = [['data is data'], ['data science']];
const plain = simulate(words, wordMap, sum);
const combined = simulate(words, wordMap, sum, sum);
console.log('word count:', JSON.stringify(plain.results));
console.log('word pairs:', plain.shuffledPairs, 'without combiner ->',
    combined.shuffledPairs, 'with combiner');

const logins = [
    [
        { user: 'ali', day: '2026-11-07', status: 'failure' },
        { user: 'ali', day: '2026-11-07', status: 'success' },
        { user: 'ali', day: '2026-11-07', status: 'failure' },
    ],
    [
        { user: 'ali', day: '2026-11-07', status: 'failure' },
        { user: 'sara', day: '2026-11-07', status: 'failure' },
        { user: 'ali', day: '2026-11-08', status: 'failure' },
    ],
];
console.log('failed logins:', JSON.stringify(
    simulate(logins, failedLoginMap, sum, sum).results
));

const scores = [
    [{ batch: 'A', score: 0 }],
    [{ batch: 'A', score: 100 }, { batch: 'A', score: 100 },
     { batch: 'A', score: 100 }],
];
const scoreMap = row => [[row.batch, [row.score, 1]]];
console.log('batch means:', JSON.stringify(
    simulate(scores, scoreMap, meanStats, mergeStats).results
));
