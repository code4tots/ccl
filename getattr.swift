import Foundation

class Thing: NSObject {
    func getattr2(runtime: Runtime, attr: NSString) {
        runtime.errorMessage = "Unknown attribute \(attr)"
    }
}

extension NSObject {
    func getattr(runtime: Runtime, attr: NSString) {
        // Unfortunately, extensions in swift cannot be overriden yet.
        // As such, this has to be done manually here.
        if let me = self as? NSNumber {
            switch attr {
            case "+":
                if let x = runtime.context.valueStack.last as? NSNumber {
                    runtime.context.valueStack.append(NSNumber(double: me.doubleValue+x.doubleValue))
                } else {
                    runtime.errorMessage = "Expected NSNumber but got \(runtime.context.valueStack.last)"
                }
                return;
            default: break;
            }
        } else if let me = self as? NSString {
            switch attr {
            case "size":
                runtime.context.valueStack.append(NSNumber(integer: me.length))
                return;
            default: break;
            }
        } else if let me = self as? NSMutableArray {
            switch attr {
            case "size":
                runtime.context.valueStack.append(NSNumber(integer: me.count))
                return;
            default: break;
            }
        } else if let me = self as? NSMutableDictionary {
            switch attr {
            case "size":
                runtime.context.valueStack.append(NSNumber(integer: me.count))
                return;
            default: break;
            }
        } else if let me = self as? Thing {
            me.getattr2(runtime, attr: attr)
            return;
        }
        runtime.errorMessage = "Unknown attribute \(attr) for object of type \(self.dynamicType)"
    }
}
