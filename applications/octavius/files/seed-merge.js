// Merges the seed dump (restored into SEED_DB) into the live DB without
// overwriting anything that already exists:
//  - documents missing from live (by _id) are inserted
//  - fields missing from an existing document are added
//  - array entries missing from an existing array are appended
//    (matched by collectionCode, then _id, then whole value)
// Run with: mongosh <uri> seed-merge.js

const SEED_DB = "OCTAVIUS_seed";
const LIVE_DB = "OCTAVIUS";

const seedDb = db.getSiblingDB(SEED_DB);
const liveDb = db.getSiblingDB(LIVE_DB);

const isPlainObject = v =>
  v !== null &&
  typeof v === "object" &&
  !Array.isArray(v) &&
  !(v instanceof Date) &&
  !v._bsontype;

const sameValue = (a, b) => EJSON.stringify(a) === EJSON.stringify(b);

const sameEntry = (a, b) => {
  if (isPlainObject(a) && isPlainObject(b)) {
    if (a.collectionCode !== undefined && b.collectionCode !== undefined) {
      return a.collectionCode === b.collectionCode;
    }
    if (a._id !== undefined && b._id !== undefined) {
      return sameValue(a._id, b._id);
    }
  }
  return sameValue(a, b);
};

// Collects $set operations for anything in seed that is missing from live
const collectMissing = (seed, live, path, set) => {
  for (const key of Object.keys(seed)) {
    const p = path ? `${path}.${key}` : key;
    const s = seed[key];
    const l = live[key];

    if (!(key in live)) {
      set[p] = s;
    } else if (isPlainObject(s) && isPlainObject(l)) {
      collectMissing(s, l, p, set);
    } else if (Array.isArray(s) && Array.isArray(l)) {
      const missing = s.filter(se => !l.some(le => sameEntry(se, le)));
      if (missing.length) set[p] = l.concat(missing);
    }
    // Otherwise live already has a value for this field: keep it
  }
};

for (const name of seedDb.getCollectionNames()) {
  const seedColl = seedDb.getCollection(name);
  const liveColl = liveDb.getCollection(name);
  let inserted = 0;
  let updated = 0;

  for (const idx of seedColl.getIndexes()) {
    if (idx.name === "_id_") continue;
    const { key, v, ns, ...options } = idx;
    liveColl.createIndex(key, options);
  }

  seedColl.find().forEach(doc => {
    const live = liveColl.findOne({ _id: doc._id });
    if (!live) {
      liveColl.insertOne(doc);
      inserted++;
      return;
    }
    const set = {};
    collectMissing(doc, live, "", set);
    if (Object.keys(set).length) {
      liveColl.updateOne({ _id: doc._id }, { $set: set });
      updated++;
    }
  });

  print(`${name}: ${inserted} inserted, ${updated} updated`);
}

seedDb.dropDatabase();
