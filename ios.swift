//
//  ios.swift
//  ccl
//
//  Created by Kyumin Kim on 7/7/15.
//  Copyright (c) 2015 Kyumin Kim. All rights reserved.
//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    var window: UIWindow?
    var runtime: Runtime?
    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        
        runtime = Runtime()
        runtime!.contexts.append(Context(opcodes: opcodes, programCounter: 0, scope: newRootScope()))
        
        self.window = UIWindow(frame: UIScreen.mainScreen().bounds)
        self.window!.backgroundColor = UIColor.whiteColor()
        self.window!.rootViewController = ViewController()
        self.window!.makeKeyAndVisible()
        return true
    }
}
class ViewController: UIViewController {
    var delegate: AppDelegate { return UIApplication.sharedApplication().delegate as! AppDelegate }
    override func viewDidLoad() {
        super.viewDidLoad()
        delegate.runtime!.run()
    }
}

