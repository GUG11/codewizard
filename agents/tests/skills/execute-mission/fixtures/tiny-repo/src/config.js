function loadConfig(env = process.env) {
  return {
    syncIntervalMs: Number(env.SYNC_INTERVAL_MS || 1000)
  };
}

module.exports = { loadConfig };
