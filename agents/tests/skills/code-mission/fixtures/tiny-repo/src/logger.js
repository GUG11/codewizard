const entries = [];

function log(message, data = {}) {
  const entry = { message, data };
  entries.push(entry);
  console.log(`${message} ${JSON.stringify(data)}`);
}

function clear() {
  entries.length = 0;
}

function getEntries() {
  return entries.slice();
}

module.exports = { clear, getEntries, log };
