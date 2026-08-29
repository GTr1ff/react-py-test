import { ModeToggle } from "@/components/ModeToggle";

// Update this page (the content is just a fallback if you fail to update the page)

const PROJECT_NAME = "Reactpy";

const Index = () => {

  return (<div className="relative flex min-h-screen items-center justify-center bg-background">
    <div className="absolute right-4 top-4 flex items-center gap-2">
      <ModeToggle />
    </div>
    <div className="text-center">
      <h1 className="mb-4 text-4xl font-bold">{PROJECT_NAME}</h1>
      <p className="text-xl text-muted-foreground">Start building.</p>
    </div>
  </div>);
};

export default Index;