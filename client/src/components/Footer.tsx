import { Link } from "react-router-dom";
import { Shield, Mail, Phone, MapPin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-muted/50 border-t border-border">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <Shield className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <div className="font-bold text-foreground">KeNHA eSafety</div>
                <div className="text-xs text-muted-foreground">Smart Road Safety</div>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              Advanced road safety management system powered by AI and IoT technology.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/report" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Report Incident
                </Link>
              </li>
              <li>
                <Link to="/incidents" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  View Incidents
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Dashboard
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Contact</h3>
            <ul className="space-y-3">
              <li className="flex items-center gap-2 text-sm text-muted-foreground">
                <Phone className="w-4 h-4" />
                <span>+254 20 123 4567</span>
              </li>
              <li className="flex items-center gap-2 text-sm text-muted-foreground">
                <Mail className="w-4 h-4" />
                <span>esafety@kenha.go.ke</span>
              </li>
              <li className="flex items-center gap-2 text-sm text-muted-foreground">
                <MapPin className="w-4 h-4" />
                <span>Nairobi, Kenya</span>
              </li>
            </ul>
          </div>

          {/* Emergency */}
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Emergency</h3>
            <div className="bg-emergency/10 border border-emergency rounded-lg p-4">
              <p className="text-sm font-semibold text-emergency mb-2">Emergency Hotline</p>
              <p className="text-2xl font-bold text-emergency">999</p>
              <p className="text-xs text-muted-foreground mt-2">Available 24/7</p>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-border text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} KeNHA eSafety. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
