; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [5 x i8]* @"True" to i8*
  %".3" = bitcast [6 x i8]* @"False" to i8*
  %"i" = alloca i32, i32 1
  store i32 0, i32* %"i"
  br label %"loop1"
loop1:
  %"i.1" = load i32, i32* %"i"
  %".6" = icmp slt i32 %"i.1", 5
  br i1 %".6", label %"loop1.if", label %"loop1.endif"
loop1.if:
  %"i.2" = load i32, i32* %"i"
  %"j" = alloca i32, i32 1
  store i32 %"i.2", i32* %"j"
  br label %"loop0"
loop1.endif:
  ret void
loop0:
  %"j.1" = load i32, i32* %"j"
  %".10" = icmp slt i32 %"j.1", 5
  br i1 %".10", label %"loop0.if", label %"loop0.endif"
loop0.if:
  %".12" = bitcast [4 x i8]* @"fstr0" to i8*
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12")
  %"j.2" = load i32, i32* %"j"
  %".14" = add i32 %"j.2", 1
  store i32 %".14", i32* %"j"
  %"j.3" = load i32, i32* %"j"
  %".16" = icmp slt i32 %"j.3", 5
  br i1 %".16", label %"loop0", label %"afterloop0"
loop0.endif:
  %".19" = bitcast [2 x i8]* @"fstr1" to i8*
  %".20" = call i32 (i8*, ...) @"printf"(i8* %".19")
  %".21" = bitcast [2 x i8]* @"fstr2" to i8*
  %".22" = call i32 (i8*, ...) @"printf"(i8* %".21")
  %"i.3" = load i32, i32* %"i"
  %".23" = add i32 %"i.3", 1
  store i32 %".23", i32* %"i"
  %"i.4" = load i32, i32* %"i"
  %".25" = icmp slt i32 %"i.4", 5
  br i1 %".25", label %"loop1", label %"afterloop1"
afterloop0:
  br label %"loop0.endif"
afterloop1:
  br label %"loop1.endif"
}

declare i32 @"printf"(i8* %".1", ...) 

@"True" = internal constant [5 x i8] c"True\00"
@"False" = internal constant [6 x i8] c"False\00"
@"fstr0" = internal constant [4 x i8] c" * \00"
@"fstr1" = internal constant [2 x i8] c" \00"
@"fstr2" = internal constant [2 x i8] c"\0a\00"