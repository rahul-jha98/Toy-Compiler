; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [5 x i8]* @"True" to i8*
  %".3" = bitcast [6 x i8]* @"False" to i8*
  %"a" = alloca i32, i32 1
  store i32 2, i32* %"a"
  %"a.1" = load i32, i32* %"a"
  %".5" = icmp eq i32 %"a.1", 2
  br i1 %".5", label %"entry.if", label %"entry.else"
entry.if:
  %".7" = bitcast [4 x i8]* @"fstr0" to i8*
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 5)
  %".9" = bitcast [2 x i8]* @"fstr1" to i8*
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9")
  %"a.2" = load i32, i32* %"a"
  %"b" = alloca i32, i32 1
  store i32 %"a.2", i32* %"b"
  %".12" = mul i32 4, 8
  %".13" = bitcast [4 x i8]* @"fstr2" to i8*
  %".14" = call i32 (i8*, ...) @"printf"(i8* %".13", i32 %".12")
  %".15" = bitcast [2 x i8]* @"fstr3" to i8*
  %".16" = call i32 (i8*, ...) @"printf"(i8* %".15")
  %"b.1" = load i32, i32* %"b"
  %".17" = bitcast [4 x i8]* @"fstr4" to i8*
  %".18" = call i32 (i8*, ...) @"printf"(i8* %".17", i32 %"b.1")
  %".19" = bitcast [2 x i8]* @"fstr5" to i8*
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".19")
  br label %"entry.endif"
entry.else:
  %"a.3" = load i32, i32* %"a"
  %".22" = icmp eq i32 %"a.3", 3
  br i1 %".22", label %"entry.else.if", label %"entry.else.else"
entry.endif:
  %".37" = icmp eq i32 2, 3
  br i1 %".37", label %"entry.endif.if", label %"entry.endif.else"
entry.else.if:
  %"a.4" = load i32, i32* %"a"
  %".24" = add i32 %"a.4", 1
  %"b.2" = alloca i32, i32 1
  store i32 %".24", i32* %"b.2"
  %"b.3" = load i32, i32* %"b.2"
  %".26" = bitcast [4 x i8]* @"fstr6" to i8*
  %".27" = call i32 (i8*, ...) @"printf"(i8* %".26", i32 %"b.3")
  %".28" = bitcast [2 x i8]* @"fstr7" to i8*
  %".29" = call i32 (i8*, ...) @"printf"(i8* %".28")
  br label %"entry.else.endif"
entry.else.else:
  %".31" = bitcast [5 x i8]* @"fstr8" to i8*
  %".32" = call i32 (i8*, ...) @"printf"(i8* %".31")
  %".33" = bitcast [2 x i8]* @"fstr9" to i8*
  %".34" = call i32 (i8*, ...) @"printf"(i8* %".33")
  br label %"entry.else.endif"
entry.else.endif:
  br label %"entry.endif"
entry.endif.if:
  %".39" = call i32 (i8*, ...) @"printf"(i8* %".2")
  br label %"entry.endif.endif"
entry.endif.else:
  %".41" = call i32 (i8*, ...) @"printf"(i8* %".3")
  br label %"entry.endif.endif"
entry.endif.endif:
  %".43" = bitcast [2 x i8]* @"fstr10" to i8*
  %".44" = call i32 (i8*, ...) @"printf"(i8* %".43")
  ret void
}

declare i32 @"printf"(i8* %".1", ...) 

@"True" = internal constant [5 x i8] c"True\00"
@"False" = internal constant [6 x i8] c"False\00"
@"fstr0" = internal constant [4 x i8] c"%d \00"
@"fstr1" = internal constant [2 x i8] c"\0a\00"
@"fstr2" = internal constant [4 x i8] c"%d \00"
@"fstr3" = internal constant [2 x i8] c"\0a\00"
@"fstr4" = internal constant [4 x i8] c"%d \00"
@"fstr5" = internal constant [2 x i8] c"\0a\00"
@"fstr6" = internal constant [4 x i8] c"%d \00"
@"fstr7" = internal constant [2 x i8] c"\0a\00"
@"fstr8" = internal constant [5 x i8] c"else\00"
@"fstr9" = internal constant [2 x i8] c"\0a\00"
@"fstr10" = internal constant [2 x i8] c"\0a\00"