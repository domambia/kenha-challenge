import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { 
  Shield, 
  AlertCircle, 
  Camera, 
  Radio, 
  Zap, 
  Users, 
  TrendingUp,
  CheckCircle2,
  ArrowRight
} from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import heroImage from "@/assets/hero-highway.jpg";
import emergencyIcon from "@/assets/emergency-icon.jpg";
import aiIcon from "@/assets/ai-verification.jpg";

const Landing = () => {
  const features = [
    {
      icon: <AlertCircle className="w-8 h-8" />,
      title: "Real-Time Incident Reporting",
      description: "Report road incidents instantly with photo and location capture. Anonymous reporting supported.",
      color: "emergency"
    },
    {
      icon: <Camera className="w-8 h-8" />,
      title: "AI-Powered Verification",
      description: "Advanced AI analyzes incidents using CCTV feeds and IoT sensors for accurate validation.",
      color: "trust"
    },
    {
      icon: <Radio className="w-8 h-8" />,
      title: "IoT Integration",
      description: "RFID readers, CCTV cameras, and multiple sensor types provide comprehensive road monitoring.",
      color: "primary"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Rapid Response Coordination",
      description: "Automated dispatch system coordinates emergency services, police, and maintenance crews efficiently.",
      color: "warning"
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: "Multi-Role Access",
      description: "17 specialized user roles from TMC operators to field inspectors, each with tailored interfaces.",
      color: "trust"
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: "Analytics & Insights",
      description: "Comprehensive dashboards with incident heatmaps, trends, and predictive analytics.",
      color: "primary"
    }
  ];

  const stats = [
    { value: "24/7", label: "Monitoring" },
    { value: "1000+", label: "IoT Sensors" },
    { value: "<5min", label: "Response Time" },
    { value: "95%", label: "Accuracy" }
  ];

  const howItWorks = [
    {
      step: "1",
      title: "Incident Detection",
      description: "System detects incidents through public reports, IoT sensors, or CCTV feeds"
    },
    {
      step: "2",
      title: "AI Verification",
      description: "AI analyzes multiple data sources to verify incident details and severity"
    },
    {
      step: "3",
      title: "Automated Dispatch",
      description: "System automatically assigns and dispatches appropriate response teams"
    },
    {
      step: "4",
      title: "Real-Time Tracking",
      description: "Monitor response progress and incident resolution in real-time"
    }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative pt-24 pb-16 md:pt-32 md:pb-24 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img 
            src={heroImage} 
            alt="Smart Highway System" 
            className="w-full h-full object-cover opacity-20"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background/50 via-background/80 to-background" />
        </div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full mb-6 border border-primary/20">
              <Shield className="w-4 h-4" />
              <span className="text-sm font-medium">Smart Road Safety Management</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold mb-6 text-foreground">
              Making Kenya's Roads
              <span className="text-primary"> Safer</span> with AI & IoT
            </h1>
            
            <p className="text-lg md:text-xl text-muted-foreground mb-8">
              Advanced incident detection, AI verification, and coordinated emergency response 
              system protecting Kenya's national highways 24/7.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/report">
                <Button size="lg" className="w-full sm:w-auto group">
                  Report Incident
                  <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link to="/dashboard">
                <Button size="lg" variant="outline" className="w-full sm:w-auto">
                  View Dashboard
                </Button>
              </Link>
            </div>
          </div>
          
          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16 max-w-4xl mx-auto">
            {stats.map((stat, index) => (
              <Card key={index} className="p-6 text-center bg-card/50 backdrop-blur border-border/50">
                <div className="text-3xl md:text-4xl font-bold text-primary mb-2">{stat.value}</div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-16 md:py-24 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
              Comprehensive Safety Features
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Leveraging cutting-edge technology to detect, verify, and respond to road incidents efficiently
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="p-6 hover:shadow-lg transition-all border-border bg-card group hover:-translate-y-1">
                <div className={`w-14 h-14 rounded-lg bg-${feature.color}/10 flex items-center justify-center mb-4 text-${feature.color} group-hover:scale-110 transition-transform`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-foreground">{feature.title}</h3>
                <p className="text-muted-foreground">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 md:py-24">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
              How It Works
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              From incident detection to resolution in four seamless steps
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {howItWorks.map((item, index) => (
              <div key={index} className="relative">
                <Card className="p-6 h-full bg-card border-border hover:border-primary transition-all">
                  <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xl font-bold mb-4">
                    {item.step}
                  </div>
                  <h3 className="text-lg font-semibold mb-2 text-foreground">{item.title}</h3>
                  <p className="text-sm text-muted-foreground">{item.description}</p>
                </Card>
                {index < howItWorks.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-3 w-6 h-0.5 bg-border" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Showcase */}
      <section className="py-16 md:py-24 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6 text-foreground">
                Advanced Technology Stack
              </h2>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-foreground mb-1">AI-Powered Analysis</h4>
                    <p className="text-muted-foreground">YOLOv8 object detection and advanced confidence scoring</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-foreground mb-1">IoT Integration</h4>
                    <p className="text-muted-foreground">RFID readers, CCTV cameras, and multi-type sensors</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-foreground mb-1">Blockchain Security</h4>
                    <p className="text-muted-foreground">Immutable incident records and evidence management</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-6 h-6 text-primary mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="font-semibold text-foreground mb-1">Real-Time Tracking</h4>
                    <p className="text-muted-foreground">Live responder location and incident status updates</p>
                  </div>
                </div>
              </div>
              <div className="mt-8">
                <Link to="/register">
                  <Button size="lg">
                    Get Started Today
                  </Button>
                </Link>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <Card className="p-6 bg-card border-border">
                <img src={emergencyIcon} alt="Emergency Response" className="w-full h-32 object-cover rounded-lg mb-4" />
                <h4 className="font-semibold text-foreground mb-2">Emergency Response</h4>
                <p className="text-sm text-muted-foreground">Coordinated multi-agency dispatch</p>
              </Card>
              <Card className="p-6 bg-card border-border">
                <img src={aiIcon} alt="AI Verification" className="w-full h-32 object-cover rounded-lg mb-4" />
                <h4 className="font-semibold text-foreground mb-2">AI Verification</h4>
                <p className="text-sm text-muted-foreground">Intelligent incident validation</p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Make Roads Safer?
          </h2>
          <p className="text-lg opacity-90 mb-8 max-w-2xl mx-auto">
            Join thousands of users helping keep Kenya's roads safe. Report incidents, track responses, and contribute to safer highways.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/report">
              <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                Report an Incident
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline" className="w-full sm:w-auto bg-transparent border-primary-foreground text-primary-foreground hover:bg-primary-foreground/10">
                Login to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Landing;
