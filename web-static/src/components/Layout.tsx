import React from "react";
import { Link, useLocation } from "react-router-dom";
import { LayoutDashboard, Beef, BookOpen, ShoppingCart, BarChart3, Menu, User } from "lucide-react";
import { ModeToggle } from "@/components/ModeToggle";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Switch } from "@/components/ui/switch";
import { toast } from "sonner";

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const [mfaEnabled, setMfaEnabled] = React.useState(false);

  const navItems = [
    { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { path: "/pantry", label: "Pantry", icon: Beef },
    { path: "/recipes", label: "Recipes", icon: BookOpen },
    { path: "/shopping-list", label: "Shopping List", icon: ShoppingCart },
    { path: "/analytics", label: "Analytics", icon: BarChart3 },
  ];

  const isActive = (path: string) => {
    if (path === "/dashboard" && location.pathname === "/") return true;
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen flex flex-col bg-amber-50/30 dark:bg-zinc-950 text-foreground">
      {/* Top Header */}
      <header className="sticky top-0 z-40 w-full border-b border-amber-100 dark:border-zinc-800 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md">
        <div className="flex h-16 items-center justify-between px-4 md:px-6 max-w-[1400px] mx-auto">
          <div className="flex items-center gap-4">
            {/* Mobile Nav Trigger */}
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden text-amber-800 dark:text-amber-200">
                  <Menu className="h-5 w-5" />
                  <span className="sr-only">Toggle Menu</span>
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="w-64 bg-white dark:bg-zinc-900 p-0">
                <div className="flex flex-col h-full">
                  <div className="h-16 flex items-center px-6 border-b border-amber-100 dark:border-zinc-800">
                    <Link to="/dashboard" className="flex items-center gap-2 font-bold text-xl text-amber-600 dark:text-amber-400">
                      <Beef className="h-6 w-6 text-amber-500" />
                      <span>PantryPal</span>
                    </Link>
                  </div>
                  <nav className="flex-1 px-4 py-4 space-y-1">
                    {navItems.map((item) => {
                      const Icon = item.icon;
                      const active = isActive(item.path);
                      return (
                        <Link
                          key={item.path}
                          to={item.path}
                          className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                            active
                              ? "bg-amber-500 text-white shadow-sm"
                              : "text-zinc-600 dark:text-zinc-400 hover:bg-amber-50 dark:hover:bg-zinc-800 hover:text-amber-600 dark:hover:text-amber-400"
                          }`}
                        >
                          <Icon className="h-5 w-5" />
                          {item.label}
                        </Link>
                      );
                    })}
                  </nav>
                </div>
              </SheetContent>
            </Sheet>

            <Link to="/dashboard" className="flex items-center gap-2 font-bold text-xl text-amber-600 dark:text-amber-400">
              <Beef className="h-6 w-6 text-amber-500" />
              <span className="tracking-tight">PantryPal</span>
            </Link>
          </div>

          <div className="flex items-center gap-4">
            {/* Account Settings Dialog */}
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="ghost" size="icon" className="text-amber-800 dark:text-amber-200" title="Account Settings">
                  <User className="h-5 w-5" />
                  <span className="sr-only">Account Settings</span>
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-white dark:bg-zinc-900 border-amber-100 dark:border-zinc-800">
                <DialogHeader>
                  <DialogTitle className="text-xl font-bold text-zinc-900 dark:text-zinc-50">
                    Account Settings
                  </DialogTitle>
                  <DialogDescription className="text-zinc-500 dark:text-zinc-400 text-xs">
                    Manage your identity, security preferences, and account lifecycle.
                  </DialogDescription>
                </DialogHeader>

                <div className="space-y-6 py-4">
                  {/* Credential Validation Engine */}
                  <div className="flex items-center justify-between p-3 rounded-xl border border-amber-50 dark:border-zinc-800/50 bg-amber-50/10">
                    <div className="space-y-0.5">
                      <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Credential Validation</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">Verify your current session credentials.</p>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-amber-200 hover:bg-amber-50 dark:border-zinc-800 dark:hover:bg-zinc-800 text-xs"
                      onClick={() => toast.success("Credentials validated successfully")}
                      data-usecases="credential-validation-engine-e24649e6"
                    >
                      Validate
                    </Button>
                  </div>

                  {/* Multi-Factor Authentication Provider */}
                  <div className="flex items-center justify-between p-3 rounded-xl border border-amber-50 dark:border-zinc-800/50 bg-amber-50/10">
                    <div className="space-y-0.5">
                      <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Multi-Factor Authentication</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">Secure your account with a secondary factor.</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Switch
                        checked={mfaEnabled}
                        onCheckedChange={(checked) => {
                          setMfaEnabled(checked);
                          toast.success(checked ? "MFA enabled successfully" : "MFA disabled");
                        }}
                        data-usecases="multi-factor-authentication-provider-95e2ce1c"
                      />
                    </div>
                  </div>

                  {/* Account Recovery Service */}
                  <div className="flex items-center justify-between p-3 rounded-xl border border-amber-50 dark:border-zinc-800/50 bg-amber-50/10">
                    <div className="space-y-0.5">
                      <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Account Recovery</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">Reset your password or recover your account.</p>
                    </div>
                    <Button
                      size="sm"
                      variant="outline"
                      className="border-amber-200 hover:bg-amber-50 dark:border-zinc-800 dark:hover:bg-zinc-800 text-xs"
                      onClick={() => toast.success("Password reset link sent to your email")}
                      data-usecases="account-recovery-service-c869f9c7"
                    >
                      Reset Password
                    </Button>
                  </div>

                  {/* Identity Lifecycle Manager */}
                  <div className="flex items-center justify-between p-3 rounded-xl border border-red-100 dark:border-red-900/30 bg-red-50/10">
                    <div className="space-y-0.5">
                      <p className="text-sm font-semibold text-red-600 dark:text-red-400">Delete Account</p>
                      <p className="text-xs text-zinc-500 dark:text-zinc-400">Permanently delete your profile and data.</p>
                    </div>
                    <Button
                      size="sm"
                      variant="destructive"
                      className="text-xs"
                      onClick={() => toast.error("Account deletion is disabled in demo mode")}
                      data-usecases="identity-lifecycle-manager-afe0ca6a"
                    >
                      Delete
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>

            <ModeToggle />
          </div>
        </div>
      </header>

      <div className="flex-1 flex max-w-[1400px] w-full mx-auto">
        {/* Persistent Left Sidebar for Desktop */}
        <aside className="hidden md:flex flex-col w-64 border-r border-amber-100 dark:border-zinc-800 bg-white dark:bg-zinc-900/50 p-4 space-y-1 shrink-0">
          <div className="px-3 py-2 mb-4">
            <p className="text-xs font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wider">
              Navigation
            </p>
          </div>
          <nav className="space-y-1 flex-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${
                    active
                      ? "bg-amber-500 text-white shadow-md shadow-amber-500/20 translate-x-1"
                      : "text-zinc-600 dark:text-zinc-400 hover:bg-amber-50 dark:hover:bg-zinc-800 hover:text-amber-600 dark:hover:text-amber-400"
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
          <div className="p-3 border-t border-amber-100 dark:border-zinc-800 text-xs text-zinc-400 dark:text-zinc-500">
            PantryPal v1.0.0
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 p-4 md:p-6 lg:p-8 overflow-x-hidden">
          <div className="max-w-[1200px] mx-auto w-full">
            {children}
          </div>
        </main>
      </div>

      {/* Mobile Sticky Bottom Navigation Bar */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white dark:bg-zinc-900 border-t border-amber-100 dark:border-zinc-800 flex justify-around py-2 px-4 shadow-lg">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center gap-1 px-2 py-1 rounded-md text-[10px] font-medium transition-colors ${
                active
                  ? "text-amber-600 dark:text-amber-400"
                  : "text-zinc-500 dark:text-zinc-400 hover:text-amber-500"
              }`}
            >
              <Icon className="h-5 w-5" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
};
