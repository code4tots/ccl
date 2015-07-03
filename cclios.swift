/*

iOS bindings for ccl.swift

Add a file named 'code.ccl' to your xcode project with the ccl code..

*/

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?
    var code : String?
    var context: Context?
    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        test() // for debugging
        let path = NSBundle.mainBundle().pathForResource("code", ofType: "ccl")!
        code = NSString(contentsOfFile: path, encoding: NSUTF8StringEncoding, error: nil)! as String
        self.window = UIWindow(frame: UIScreen.mainScreen().bounds)
        self.window!.backgroundColor = UIColor.whiteColor()
        self.window!.rootViewController = ViewController()
        self.context = ContextFromCode(code!)
        self.window!.makeKeyAndVisible()
        return true
    }
}
class ViewController: UIViewController {
    var delegate : AppDelegate { return UIApplication.sharedApplication().delegate as! AppDelegate }
    var context : Context { return delegate.context! }
    override func viewDidLoad() {
        super.viewDidLoad()
        context.root["window"] = WindowThing(fromAnyObject: delegate)
        context.root["new-button"] = NF { (c:Context) in
            c.push(ButtonThing(fromAnyObject: self.delegate))
        }
        context.run()
    }
}
class UiThing : Thing {
    var delegate : AppDelegate { return x as! AppDelegate }
    var window : UIWindow { return delegate.window! }
    var controller : ViewController { return window.rootViewController as! ViewController }
    var view : UIView { return controller.view }
    override var hash : Int { return ObjectIdentifier(self).hashValue }
    override func isEqual(y: AnyObject?) -> Bool { return y != nil && ObjectIdentifier(self) == ObjectIdentifier(y!) }
    override var description : String { return "<UiThing>" }
}
class WindowThing : UiThing {
    override var description : String {
        return "<window>"
    }
    override func getattr(attr: String) -> Thing {
        switch attr {
        case "width": return Thing(floatLiteral: Double(view.bounds.width))
        case "height": return Thing(floatLiteral: Double(view.bounds.height))
        default:
            return super.getattr(attr)
        }
    }
}
extension Thing {
    var color : UIColor {
        if let s = x as? String {
            switch s {
            case "red": return UIColor.redColor()
            case "green": return UIColor.greenColor()
            case "blue": return UIColor.blueColor()
            default:
                // TODO: Error handling.
                break
            }
        }
        // TODO: RGBA list to color.
        // TODO: Error handling
        return UIColor.blackColor()
    }
}
func color2Thing(color: UIColor) -> Thing {
    var r : CGFloat = 0, g : CGFloat = 0, b : CGFloat = 0, a : CGFloat = 0
    color.getRed(&r, green: &g, blue: &b, alpha: &a)
    return [
        Thing(floatLiteral: Double(r)),
        Thing(floatLiteral: Double(g)),
        Thing(floatLiteral: Double(b)),
        Thing(floatLiteral: Double(a))
    ]
}
class ButtonThing : UiThing {
    var button : UIButton = UIButton()
    override func getattr(attr: String) -> Thing {
        switch attr {
        case "=frame":
            return NF { (c:Context) in
                let args = c.pop()
                self.button.frame = CGRectMake(CGFloat(args[0].n), CGFloat(args[1].n), CGFloat(args[2].n), CGFloat(args[3].n))
            }
        case "=title":
            return NF { (c:Context) in
                self.button.setTitle(c.pop().s as String, forState: UIControlState.Normal)
            }
        case "show":
            return NF { (c: Context) in
                self.view.addSubview(self.button)
            }
        case "=bg":
            return NF { (c: Context) in
                self.button.backgroundColor = c.pop().color
            }
        case "bg":
            return color2Thing((self.button.backgroundColor!))
//        case "=onclick":
//            return NF { (c: Context) in
//                let cb = c.pop() as! Lambda
//                self.button.addTarget(cb, action: "buttonTapAction:", forControlEvents: UIControlEvents.TouchUpInside)
//            }
        default:
            return super.getattr(attr)
        }
    }
}