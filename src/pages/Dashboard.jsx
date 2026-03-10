import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div className="container">
      <h2 className="mb-4">AI Tools Dashboard</h2>

      <div className="row g-4">

        <div className="col-md-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title">Document Chatbot</h5>
              <p className="card-text">
                Chat with your uploaded documents.
              </p>
              <Link to="/chatbot" className="btn btn-primary">
                Open Tool
              </Link>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title">Meeting Notes Generator</h5>
              <p className="card-text">
                Upload audio and generate notes.
              </p>
              <Link to="/meeting-notes" className="btn btn-primary">
                Open Tool
              </Link>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow">
            <div className="card-body">
              <h5 className="card-title">SEO Analyzer</h5>
              <p className="card-text">
                Analyze SEO performance of a website.
              </p>
              <Link to="/seo-analyzer" className="btn btn-primary">
                Open Tool
              </Link>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default Dashboard;