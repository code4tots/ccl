/*

iOS bindings for ccl.swift

Add a file named 'code.ccl' to your xcode project with the ccl code..

*/

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?
    var code : String?
    var runtime: Runtime?
    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        test() // for debugging
        let path = NSBundle.mainBundle().pathForResource("code", ofType: "ccl")!
        code = NSString(contentsOfFile: path, encoding: NSUTF8StringEncoding, error: nil)! as String
        self.window = UIWindow(frame: UIScreen.mainScreen().bounds)
        self.window!.backgroundColor = UIColor.whiteColor()
        self.window!.rootViewController = ViewController()
        self.runtime = RuntimeFromCode(code!)
        self.window!.makeKeyAndVisible()
        return true
    }
}
class ViewController: UIViewController {
    var delegate : AppDelegate { return UIApplication.sharedApplication().delegate as! AppDelegate }
    var runtime : Runtime { return delegate.runtime! }
    override func viewDidLoad() {
        super.viewDidLoad()
        runtime.root["window"] = WindowThing(fromAnyObject: delegate)
        runtime.root["new-button"] = NF { (c:Runtime) in
            c.push(ButtonThing(fromAnyObject: self.delegate))
        }
        runtime.run()
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
    override var description : String {
        return "<button \(button)>"
    }
    var button : UIButton = UIButton()
    var handler : ButtonActionHandler?
    override func getattr(attr: String) -> Thing {
        switch attr {
        case "frame=":
            return NF { (c:Runtime) in
                let args = c.pop()
                self.button.frame = CGRectMake(CGFloat(args[0].n), CGFloat(args[1].n), CGFloat(args[2].n), CGFloat(args[3].n))
            }
        case "title=":
            return NF { (c:Runtime) in
                self.button.setTitle(c.pop().s as String, forState: UIControlState.Normal)
            }
        case "show":
            return NF { (c: Runtime) in
                self.view.addSubview(self.button)
            }
        case "bg=":
            return NF { (c: Runtime) in
                self.button.backgroundColor = c.pop().color
            }
        case "bg":
            return color2Thing((self.button.backgroundColor!))
        case "onclick=":
            return NF { (c: Runtime) in
                let v = c.pop()
                if let b = v as? Block {
                    self.handler = ButtonActionHandler(c, b)
                    self.button.addTarget(self.handler, action: "buttonTapAction:", forControlEvents: UIControlEvents.TouchUpInside)
                } else {
                    assert(false, "\(v) needs to be a block to set to onclick")
                }
            }
        default:
            return super.getattr(attr)
        }
    }
}
class ButtonActionHandler : NSObject {
    var runtime : Runtime
    var block : Block
    init(_ c: Runtime, _ b : Block) {
        runtime = c
        block = b
    }
    func buttonTapAction(sender: AnyObject?) {
        println("tap action")
        runtime.summon(block)
    }
}
