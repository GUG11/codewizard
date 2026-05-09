function parseItems(input) {
  if (input === "") {
    throw new Error("Cannot parse empty input");
  }

  return input.split(",").map((item) => item.trim().toLowerCase());
}

module.exports = { parseItems };
