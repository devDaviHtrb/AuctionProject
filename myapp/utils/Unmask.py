def unmask(var):
    var = var.replace(" ", "")
    var =  var.replace("\n", "")
    var = var.replace("(", "")
    var = var.replace(")", "")
    var = var.replace("-", "")
    var = var.replace(".", "")
    return var