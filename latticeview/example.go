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

	for _, a := range lattice.Atoms {
		sphere := geometry.NewSphere(float64(a.Radius)/100, 64, 64, 0, math32.Pi*2, 0, math32.Pi*2)
		mat := material.NewPhong(math32.NewColor("DarkBlue"))
		sphereMesh := graphic.NewMesh(sphere, mat)
		sphereMesh.SetPosition(a.X/100, a.Y/100, a.Z/100)
		app.Scene().Add(sphereMesh)
	}

	// Add lights to the scene
	color := math32.NewColor("White")
	ambientLight := light.NewAmbient(color, 1.0)
	app.Scene().Add(ambientLight)
	//pointLight := light.NewPoint(color, 5.0)
	//pointLight.SetPosition(1, 0, 2)
	//app.Scene().Add(pointLight)

	// Add an axis helper to the scene
	axis := graphic.NewAxisHelper(1.0)
	app.Scene().Add(axis)

	// Create a blue torus and add it to the scene
	// geom := geometry.NewTorus(1, .4, 12, 32, math32.Pi*2)
	// mat := material.NewPhong(math32.NewColor("DarkBlue"))
	// torusMesh := graphic.NewMesh(geom, mat)
	// torusMesh.SetPosition(1.0, 1.0, 1.0)
	// app.Scene().Add(torusMesh)

	// Add lights to the scene
	// color := math32.NewColor("White")
	// ambientLight := light.NewAmbient(color, 0.8)
	// app.Scene().Add(ambientLight)
	// pointLight := light.NewPoint(color, 5.0)
	// pointLight.SetPosition(1, 0, 2)
	// app.Scene().Add(pointLight)

	// Add an axis helper to the scene
	// axis := graphic.NewAxisHelper(0.5)
	// app.Scene().Add(axis)

	app.CameraPersp().SetPosition(0, 0, 3)
	app.Run()
}
