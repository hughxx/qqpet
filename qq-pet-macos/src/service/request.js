module.exports = function offlineRequest() { return Promise.reject(new Error("offline-only")); };
