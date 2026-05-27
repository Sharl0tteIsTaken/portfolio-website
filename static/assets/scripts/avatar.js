function useBackupBrandImage(image) {
    image.onerror = "";
    image.src = "static\assets\img\github-avatar.jfif";
    // TODO: change this ^ in refactor js files (`\` -> `/`)
    // TODO: refactor all JS files:
    // TODO: 1. use `arrow function` and `const` or `let`
    // TODO: 2. don't leak into global scope
    return true;
}
