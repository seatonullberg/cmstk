package main

import (
	"log"
	"os"

	"github.com/g3n/engine/geometry"
	"github.com/g3n/engine/graphic"
	"github.com/g3n/engine/light"
	"github.com/g3n/engine/material"
	"github.com/g3n/engine/math32"
	"github.com/g3n/engine/util/application"

	"github.com/seatonullberg/cmstk/latticeview/latticeview"
)

func main() {

	path := os.Args[1] // only accept one file right now
	lattice, err := latticeview.ReadProtoFile(path)
	if err != nil {
		log.Fatal(err)
	}

	app, _ := application.Create(application.Options{
		Title:  "LatticeView",
		Width:  800,
		Height: 800,
	})

	// Populate the scene with atoms
	for _, a := range lattice.Atoms {
		radius := float64(a.Radius) / 100
		sphere := geometry.NewSphere(radius, 64, 64, 0, math32.Pi*2, 0, math32.Pi*2)
		mat := material.NewPhong(math32.NewColor("DarkBlue"))
		sphereMesh := graphic.NewMesh(sphere, mat)
		sphereMesh.SetPosition(a.X/100, a.Y/100, a.Z/100)
		app.Scene().Add(sphereMesh)
	}

	// Add lights to the scene
	lightColor := math32.NewColor("White")
	ambientLight := light.NewAmbient(lightColor, 0.8)
	app.Scene().Add(ambientLight)
	pointLight := light.NewPoint(lightColor, 5.0)
	pointLight.SetPosition(-2, -2, -2)
	app.Scene().Add(pointLight)

	// Add an axis helper to the scene
	axis := graphic.NewAxisHelper(1.0)
	axis.SetPosition(-1, -1, -1)
	app.Scene().Add(axis)

	// Set camera position
	app.CameraPersp().SetPosition(0, 0, 5)
	app.Run()
}
