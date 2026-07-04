let loadCount = 0;

function loadDashboard(userId) {
  loadCount += 1;
  return {
    userId,
    loadCount,
    widgets: ["activity", "usage", "alerts"]
  };
}

function getLoadCount() {
  return loadCount;
}

function resetLoadCount() {
  loadCount = 0;
}

module.exports = { getLoadCount, loadDashboard, resetLoadCount };
