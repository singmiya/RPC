namespace py pi # 生成python代码以pi为包名

struct PiRequest {
    1:i32 n
}

struct PiResponse {
    1:double value
}

exception IllegalArgument {
    1:string message
}

service PiService {
    PiResponse calc(1:PiRequest req) throws(1:IllegalArgument ia)
}