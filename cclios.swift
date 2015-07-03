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
        ccltest() // for debugging
        let path = NSBundle.mainBundle().pathForResource("code", ofType: "ccl")!
        code = NSString(contentsOfFile: path, encoding: NSUTF8StringEncoding, error: nil)! as String
        self.window = UIWindow(frame: UIScreen.mainScreen().bounds)
        self.window!.backgroundColor = UIColor.whiteColor()
        self.window!.rootViewController = ViewController()
        self.context = RootContext()
        self.context!["window"] = WindowThing(self)
        self.context!["new-button"] = Verb { (c:Context) in
            c.push(ButtonThing(self))
        }
        self.window!.makeKeyAndVisible()
        return true
    }
}

class UiThing : Thing {
    var app : AppDelegate
    var view : UIView {
        return app.window!.rootViewController!.view
    }
    override var hashValue : Int {
        return ObjectIdentifier(self).hashValue
    }
    override func eq2(rhs: Thing) -> Bool {
        return ObjectIdentifier(self) == ObjectIdentifier(rhs)
    }
    override var truthy : Bool {
        return true
    }
    init(_ app : AppDelegate) { self.app = app }
}

class WindowThing : UiThing {
    override var description : String {
        return "<window>"
    }
    override func getattr(attr: String) -> Thing {
        switch attr {
        case "width": return Num(Double(view.bounds.width))
        case "height": return Num(Double(view.bounds.height))
        default:
            super.getattr(attr)
        }
        return Num(0)
    }
}

class ButtonThing : UiThing {
    var button : UIButton = UIButton()
    override var description : String {
        return "<button>"
    }
    override func getattr(attr: String) -> Thing {
        switch attr {
        case "=frame":
            return Verb { (c:Context) in
                let arg = c.pop()
                let args = arg as! List
                self.button.frame = CGRectMake(CGFloat((args.x[0] as! Num).x), CGFloat((args.x[1] as! Num).x), CGFloat((args.x[2] as! Num).x), CGFloat((args.x[3] as! Num).x))
            }
        case "=title":
            return Verb { (c:Context) in
                let arg = c.pop()
                if let title = arg as? Str {
                    self.button.setTitle(title.x, forState: UIControlState.Normal)
                } else {
                    assert(false, "button.=title expects a str argument")
                }
            }
        case "show":
            return Verb { (c: Context) in
                self.view.addSubview(self.button)
            }
        case "=bg":
            return Verb { (c: Context) in
                self.button.backgroundColor = str2color((c.pop() as! Str).x)
                
            }
        case "bg":
            return Str(color2str(self.button.backgroundColor!))
        case "=onclick":
            return Verb { (c: Context) in
                let cb = c.pop() as! Lambda
                self.button.addTarget(cb, action: "buttonTapAction:", forControlEvents: UIControlEvents.TouchUpInside)
            }
        default:
            return super.getattr(attr)
        }
    }
}

func str2color(s: String) -> UIColor {
    switch s {
    case "green": return UIColor.greenColor()
    case "blue": return UIColor.blueColor()
    case "brown": return UIColor.brownColor()
    case "red": return UIColor.redColor()
    default:
        assert(false, "\(s) is not a supported color")
        return UIColor.blackColor()
    }
}

func color2str(c: UIColor) -> String {
    switch c {
    case UIColor.greenColor(): return "green"
    case UIColor.blueColor(): return "blue"
    case UIColor.brownColor(): return "brown"
    case UIColor.redColor(): return "red"
    default: return ""
    }
}

class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        let delegate = UIApplication.sharedApplication().delegate as! AppDelegate
        parse(delegate.code!).exec(delegate.context!)
    }
}
