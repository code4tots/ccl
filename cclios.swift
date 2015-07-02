/*

iOS bindings for ccl.swift

Add a file named 'code.ccl' to your xcode project with the ccl code..

*/

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    
    var window: UIWindow?
    
    // CCL context
    var context: Context?
    
    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        // just for debugging
        ccltest()
        
        // Override point for customization after application launch.
        let path = NSBundle.mainBundle().pathForResource("code", ofType: "ccl")!
        let code = NSString(contentsOfFile: path, encoding: NSUTF8StringEncoding, error: nil)! as String
        
        self.window = UIWindow(frame: UIScreen.mainScreen().bounds)
        self.window!.backgroundColor = UIColor.whiteColor()
        self.window!.rootViewController = ViewController()
        
        self.context = RootContext()
        
        self.context!["window"] = WindowThing(self)
        
        parse(code).exec(self.context!)
        
        self.window!.makeKeyAndVisible()
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

class WindowThing : Thing {
    var app : AppDelegate
    
    var view : UIView {
        return app.window!.rootViewController!.view
    }
    
    init(_ app : AppDelegate) { self.app = app }
    
    override var hashValue : Int {
        return ObjectIdentifier(self).hashValue
    }
    override var description : String {
        return "<window>"
    }
    override func eq(rhs: Thing) -> Bool {
        return ObjectIdentifier(self) == ObjectIdentifier(rhs)
    }
    override var truthy : Bool {
        return true
    }
    override func getattr(attr: String) -> Thing {
        switch attr {
        case "width": return Num(Double(view.bounds.width))
        case "height": return Num(Double(view.bounds.height))
        default:
            assert(false, "WindowThing does not support attribute " + attr)
        }
        return Num(0)
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
