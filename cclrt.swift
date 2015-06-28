import UIKit

// MARK: iOS boilerplate

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    
    var window: UIWindow?
    
    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        // Override point for customization after application launch.
        return true
    }
    
    func applicationWillResignActive(application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
    }
    
    func applicationDidEnterBackground(application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }
    
    func applicationWillEnterForeground(application: UIApplication) {
        // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
    }
    
    func applicationDidBecomeActive(application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }
    
    func applicationWillTerminate(application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }
}

class ViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
}

// MARK: CCL language core

class Context {
    let table : NSMutableDictionary = NSMutableDictionary()
    let parent : Context?
    
    init(_ parent: Context?) {
        self.parent = parent
        
        if parent == nil {
            table["__stack__"] = NSMutableArray()
            
            table["print"] = Verb { (ctx) in
                print(ctx.pop())
            }
            
            table["println"] = Verb { (ctx) in
                println(ctx.pop())
            }
            
            table["true"] = true
            table["false"] = false
            
            table["if"] = Verb { (ctx) in
                ctx.stack
                let rhs = ctx.pop() as! Verb
                let lhs = ctx.pop() as! Verb
                let cond = ctx.pop() as! Verb
                
                var choice = lhs
                
                cond.x(ctx)
                
                let v: AnyObject = ctx.pop()
                
                if let b = v as? Bool {
                    choice = b ? lhs : rhs
                } else if let i = v as? Int {
                    choice = i != 0 ? lhs : rhs
                } else if let f = v as? Float {
                    choice = f != 0 ? lhs : rhs
                } else if let s = v as? String {
                    choice = s != "" ? lhs : rhs
                } else {
                    // Assume all other values are true for now
                    choice = lhs
                }
                choice.x(ctx)
            }
        }
    }
    
    subscript(key: String) -> AnyObject? {
        get {
            if let v: AnyObject = table[key] {
                return v
            } else if let p = parent {
                return p[key]
            }
            return nil
        }
        set(value) {
            if let v: AnyObject = table[key] {
                table[key] = value
            } else if let p = parent {
                p[key] = value
            }
            table[key] = value
        }
    }
    
    func push(x: AnyObject) {
        stack.addObject(x)
    }
    
    func pop() -> AnyObject {
        let ret: AnyObject = stack.lastObject!
        stack.removeLastObject()
        return ret
    }
    
    var stack : NSMutableArray {
        return (self["__stack__"] as! NSMutableArray)
    }
}

class Verb {
    let x : (Context) -> Void
    init(x : (Context) -> Void) { self.x = x }
    var description : String {
        return "xx\(x)"
    }
}

func pushvalue(ctx: Context, value: AnyObject) {
    ctx.push(value)
}

func summonid(ctx: Context, name: String) {
    if let val: AnyObject = ctx[name] {
        if let verb = val as? Verb {
            verb.x(ctx)
        } else {
            ctx.push(val)
        }
    } else {
        println("No identifier '" + name + "'\n")
        exit(1)
    }
}

func popandrun(ctx: Context) {
    let cmd = (ctx["__stack__"] as! NSMutableArray).lastObject as! Verb
    (ctx["__stack__"] as! NSMutableArray).removeLastObject()
    cmd.x(ctx)
}

var ctx = Context(nil)
