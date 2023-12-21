import React from "react";
import clsx from "clsx";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import Layout from "@theme/Layout";
import styles from "./index.module.css";

type HowToItem = {
  image: string;
  description: string;
  buttonLink?: string;
  buttonText?: string;
};

type FeatureItem = {
  image: string;
  subtitle: string;
  description: string;
  link: string;
};

export function HowToCard({
  image,
  description,
  buttonLink,
  buttonText,
}: HowToItem) {
  return (
    <div
      className={styles["feature-card"]}
      style={{
        display: "flex",
        flexDirection: "row",
        alignItems: "stretch",
        gap: "20px",
      }}
    >
      <div style={{ display: "flex", flex: 1, height: "100%" }}>
        <img src={image} style={{ borderRadius: "5px" }} />
      </div>
      <div
        style={{
          display: "flex",
          flex: 1,
          flexDirection: "column",
          justifyContent: "center",
          paddingRight: "10px",
        }}
      >
        <div className={styles["feature-card-text"]}>
          <p>{description}</p>
        </div>
        {buttonLink ? (
          <div style={{ textAlign: "center" }}>
            <a href={buttonLink} className="button button--primary">
              {buttonText}
            </a>
          </div>
        ) : null}
      </div>
    </div>
  );
}

const HowToList = [
  {
    image: "/img/index/monit-one-machine.png",
    description: "Monit running python codes on a single computer",
    buttonLink: "/docs/howto",
    buttonText: "Use on single machine",
  },
  {
    image: "/img/index/monit-machines-on-local-network.png",
    description:
      "Monit some python codes running on multiple machines connected to same network",
    buttonLink: "/docs/howto",
    buttonText: "Use on multiple machine",
  },
];

export function FeatureCard({
  image,
  subtitle,
  description,
  link,
}: FeatureItem) {
  return (
    <div
      className={styles["feature-card"]}
      style={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
      }}
    >
      <div
        style={{
          display: "flex",
          margin: "30px",
          flexDirection: "column",
          justifyContent: "center",
          flex: "50%",
        }}
      >
        <a href={link}>
          <h3 style={{ fontStyle: "italic" }}>{subtitle}</h3>
        </a>
        <div className={clsx(styles["feature-card-text"])}>
          <p>{description}</p>
        </div>
      </div>
      <div
        style={{
          display: "flex",
          flex: "50%",
          flexDirection: "column",
          justifyContent: "center",
        }}
      >
        <img
          src={image}
          style={{ boxShadow: "rgba(0, 0, 0, 0.05) 0px 0px 0px 1px" }}
        />
      </div>
    </div>
  );
}

export const FeatureList = [
  {
    image: "/img/index/neetbox-consistof.jpg",
    subtitle: "All in one",
    description:
      "Neetbox provides python side apis, command line cli app, web service, and frontend pages. Get ready by a single pip install, no registers, no extra steps, on extra configs, install and run by once. ",
    link: "/docs/howto",
  },
  {
    image: "/img/index/view-everywhere.jpg",
    subtitle: "View everywhere",
    description:
      "Monit your projects everywhere on any devides with a browser. visit neetbox frontend console on PC, tablets, even phones.",
    link: "/docs/howto",
  },
  {
    image: "/img/index/simple-apis.jpg",
    subtitle: "Easy python APIs",
    description:
      "Neetbox provides functions and function decorators for python codes. Neetbox python APIs are designed for easy purpose, they automatically connects your projects and web.",
    link: "/docs/howto",
  },
  {
    image: "/img/index/support-different-data.jpg",
    subtitle: "Send types of data",
    description:
      "Neetbox provides apis for different data types, data such as logs, images, scalars etc. are stored in history database and send to frontend automatically. View your data in a single dashboard.",
    link: "/docs/howto",
  },
  {
    image: "/img/index/monit-multiple-projects.jpg",
    subtitle: "View projects on different machines",
    description:
      "View multiple projects running on different machines remotely, or view history data when projects are offline. Select project to view in you frontend sidebar.",
    link: "/docs/howto",
  },
  {
    image: "/img/index/distinguish-runs.jpg",
    subtitle: "Manage projects and runs",
    description:
      "Neetbox knows each time your project runs. Neetbox provides Tensorboard like viewing strateg. You can specific name of a run or select which run to view in frontend.",
    link: "/docs/howto",
  },
  {
    image: "/img/index/use-actions.jpg",
    subtitle: "Remote function call",
    description:
      "Register a python function as an neetbox action, so that i appears as a button on your frontend console. Neetbox allows you to monit your running projects interactively.",
    link: "/docs/howto",
  },
  {
    image: "/img/index/monit-hardware.jpg",
    subtitle: "Check hardware usage",
    description:
      "Neetbox automatically apply hardware monitoring when project launch.",
    link: "/docs/howto",
  },
  {
    image: "/img/index/notify-errors.jpg",
    subtitle: "Notice on error",
    description:
      "Once neetbox frontend is opened in your browser, it shows notifications when there are errors or something needs attention. Solve crashes in time with neetbox.",
    link: "/docs/howto",
  },
];

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout title={`Hello from ${siteConfig.title}`} description="">
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          backgroundImage: "url('/img/index/background.jpg')",
          backgroundSize: "cover",
          backgroundRepeat: "no-repeat",
          backgroundPosition: "center",
          backgroundAttachment: "fixed",
          height: "100vh",
        }}
      >
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            paddingLeft: "10%",
            paddingRight: "10%",
            maxWidth: "90%",
            justifyContent: "center",
            paddingBottom: "var(--ifm-navbar-height)",
          }}
        >
          <h1
            style={{
              color: "white",
              textShadow: "3px 3px 3px black",
              textAlign: "center",
            }}
          >
            {siteConfig.title}
          </h1>
          <h2
            style={{
              color: "white",
              textShadow: "1px 1px 1px black",
              textAlign: "center",
            }}
          >
            A tool box for Logging / Debugging / Tracing / Managing /
            Facilitating long running python projects, especially a replacement
            of tensorboard for deep learning projects.
          </h2>
          <div style={{ paddingTop: "30px", textAlign: "center" }}>
            <a href="#howtos" className="button button--secondary">
              Try Try Need
            </a>
          </div>
        </div>
      </div>
      <div id="howtos">
        <div
          style={{
            padding: "10px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginTop: "50px",
          }}
        >
          <h2>How To</h2>
          <div
            style={{
              maxWidth: "1000px",
              display: "flex",
              flexDirection: "row",
              justifyContent: "space-evenly",
              gap: "30px",
            }}
          >
            {HowToList.map((props, idx) => (
              <div style={{ flex: 1 }}>
                <HowToCard key={idx} {...props} />
              </div>
            ))}
          </div>
          <div style={{ marginTop: "50px" }} />

          <h2>Why NEETBOX?</h2>

          <div
            style={{
              maxWidth: "1000px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-evenly",
              marginTop: "20px",
              gap: "10px",
            }}
          >
            {FeatureList.map((props, idx) => (
              <FeatureCard key={idx} {...props} />
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}
