const simpleMathTest1 = function () {
    let m = 0;
    m += 100;
    m -= 50;
    m *= 4;
    m /= 2;
    return m;
}

const simpleMathTest2 = function () {
    let m = 0;
    m += 200;
    m -= 50;
    m *= 4;
    m /= 2;
    return m;
}

const canAccessLuciferAPI = function () {
    return lucifer !== undefined;
}

const canAccessLuciferManager = function () {
    return lucifer.luciferManager !== undefined;
}

const getVersion = function () {
    return lucifer.LMI.luciferManager.version;
}
