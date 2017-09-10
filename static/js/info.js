$("#fileUpload").change(function () {
    if (this.value == this.oldvalue) return; //not changed really
    this.oldvalue = this.value;

    $("#fileForm").submit();

    return false;
});