const assert = require("assert");
const logger = require("../src/logger");
const { loadConfig } = require("../src/config");
const { getLoadCount, loadDashboard, resetLoadCount } = require("../src/dashboard");
const { parseItems } = require("../src/parser");
const { syncUsers } = require("../src/sync");

logger.clear();
assert.deepStrictEqual(syncUsers([{ id: "u1", active: true }, { id: "u2", active: false }]), ["u1"]);
assert.strictEqual(logger.getEntries().length, 1);

assert.deepStrictEqual(parseItems("A, B"), ["a", "b"]);

resetLoadCount();
assert.deepStrictEqual(loadDashboard("u1").widgets, ["activity", "usage", "alerts"]);
assert.strictEqual(getLoadCount(), 1);

assert.deepStrictEqual(loadConfig({ SYNC_INTERVAL_MS: "2500" }), { syncIntervalMs: 2500 });

console.log("tests ok");
