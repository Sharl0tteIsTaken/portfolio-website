function useBackupBrandImage(image) {
    image.onerror = "";
    image.src = "static\assets\img\github-avatar.jfif";
    return true;
}