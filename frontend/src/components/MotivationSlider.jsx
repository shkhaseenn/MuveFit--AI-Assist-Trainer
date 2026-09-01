import React, { useEffect, useState } from "react";

function MotivationSlider() {

  const slides = [

    {
      title: "Consistency beats intensity.",
      text: "Small improvements in form add up."
    },

    {
      title: "Your movement is improving.",
      text: "Your form score is up 6% this week."
    },

    {
      title: "Focus on the next rep.",
      text: "Good movement starts with good awareness."
    },

    {
      title: "Move with intention.",
      text: "Quality reps matter more than rushing."
    }

  ];


  const [active, setActive] =
    useState(0);


  useEffect(() => {

    const timer = setInterval(() => {

      setActive(
        previous =>
          (previous + 1) %
          slides.length
      );

    }, 4500);


    return () => {
      clearInterval(timer);
    };

  }, [slides.length]);


  const slide = slides[active];


  return (
    <section className="motivation-slider">

      <div className="motivation-orbit" />

      <div className="motivation-content">

        <span className="motivation-label">
          MOVE NOTE / {String(active + 1).padStart(2, "0")}
        </span>


        <h2>
          {slide.title}
        </h2>


        <p>
          {slide.text}
        </p>


        <div className="motivation-dots">

          {slides.map((_, index) => (

            <button
              key={index}
              className={
                index === active
                  ? "active"
                  : ""
              }
              onClick={() =>
                setActive(index)
              }
              aria-label={
                `Show motivation ${index + 1}`
              }
            />

          ))}

        </div>

      </div>

    </section>
  );
}

export default MotivationSlider;