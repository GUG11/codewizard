const logger = require("./logger");

function syncUsers(users = []) {
  const activeUsers = users.filter((user) => user.active);
  logger.log("syncUsers complete", { count: activeUsers.length });
  return activeUsers.map((user) => user.id);
}

module.exports = { syncUsers };
