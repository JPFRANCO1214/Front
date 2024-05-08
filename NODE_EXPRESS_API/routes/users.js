import express from 'express';

import { createUser, getUsers, getUser, deleteUser, updateUser }from '../controllers/users.js';

const router = express.Router(); 

// all routes in here are starting with /users
router.get('/', getUsers);

//Create an object
router.post('/', createUser);


//GET is used to get details
router.get('/:id' , getUser);

//delete something
router.delete('/:id', deleteUser);

router.patch('/:id', updateUser)

export default router;