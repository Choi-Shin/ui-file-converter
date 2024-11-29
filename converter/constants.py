CSV = "csv"
XLSX = "xlsx"
XLS = "xls"
JSON = "json"
PNG = "png"
JPEG = "jpeg"
JPG = "jpg"
WEBP = "webp"
AVIF = "avif"
type_map = {
    CSV: [XLSX, XLS, JSON],
    XLSX: [CSV, XLS, JSON],
    XLS: [CSV, XLSX, JSON],
    JSON: [CSV, XLS, XLSX],
    PNG: [JPEG, JPG, WEBP, AVIF],
    JPEG: [PNG, JPG, WEBP, AVIF],
    JPG: [PNG, JPEG, WEBP, AVIF],
    WEBP: [JPEG, JPG, PNG, AVIF],
    AVIF: [JPEG, JPG, WEBP, PNG],
}
